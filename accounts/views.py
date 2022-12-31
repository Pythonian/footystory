from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from .decorators import ajax_required

from story.models import Story
from notifications.models import Notification

from .forms import SignUpForm, UserForm, ProfileForm, ResendActivationEmailForm
from .tokens import account_activation_token
from .models import Profile, Follow


User = get_user_model()


def signup(request):
    if request.user.is_authenticated():
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # User shouldn't log in before confirming email
            user.is_active = False
            user.save()
            # Load profile instance created by the signal
            user.refresh_from_db()
            user.profile.favorite_club = form.cleaned_data.get('favorite_club')
            user.save()
            current_site = get_current_site(request)

            if request.is_secure():
                protocol = 'https'
            else:
                protocol = 'http'
            
            subject = render_to_string(
                'registration/account_activation_subject.txt', 
                {'site_name': current_site.name}
            )
            
            message = render_to_string(
                'registration/account_activation_email.html',
                {'user': user,
                 'domain': current_site.domain,
                 'protocol': protocol,
                 'site_name': current_site.name,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),}
            )
            user.email_user(subject, message)
            return redirect('account_activation_sent')
        else:
            messages.error(request, "An error occured while trying to create your account.")
            return render(request,
                'registration/signup.html',
                {'form': form})
    else:
        form = SignUpForm()

    template = 'registration/signup.html'
    context = {
        'form': form
    }
    
    return render(request, template, context)


def resend_activation(request):
    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email__iexact=email, is_active=False)
            if not user.count():
                form._errors['email'] = ['Account for email address is not registered or already activated.']
            current_site = get_current_site(request)
            if request.is_secure():
                protocol = 'https'
            else:
                protocol = 'http'
            subject = render_to_string(
                'registration/account_activation_subject.txt', 
                {'site_name': current_site.name}
            )
            
            message = render_to_string(
                'registration/account_activation_email.html',
                {'user': user,
                 'domain': current_site.domain,
                 'protocol': protocol,
                 'site_name': current_site.name,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),}
            )
            user.email_user(subject, message)
            return redirect('account_activation_sent')
        else:
            messages.error(request, "An error occured while sending your account activation email.")
            return redirect('resend_activation')
    else:
        form = ResendActivationEmailForm()

    template = 'registration/resend_activation.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def account_activation_sent(request):
    if request.user.is_authenticated():
        return redirect('home')

    template = 'registration/account_activation_sent.html'
    context = {}

    return render(request, template, context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Your profile has been successully created.')
        return redirect('home')
    else:
        return render(
            request,
            'registration/activate.html',
            {})


@login_required
def disable(request, username):
    user = get_object_or_404(
        User, username=username)
    if request.method == 'POST':
        # Disable the user's password
        user.set_unusable_password()
        # Disable the user's account
        user.is_active = False
        user.save()
        logout(request)
        return redirect('home')

    template = 'accounts/disable.html'
    context = {}

    return render(request, template, context)


def profile(request, username):
    user = get_object_or_404(
        User, username=username)
    followers = user.profile.get_followers()
    followings = user.profile.get_following()[:2]
    is_following = False
    if request.user in followers:
        is_following = True

    latest_stories = Story.published.filter(author=user)[:3]
    recommends = user.stories_favorited.filter(status=Story.PUBLISHED)[:3]

    drafts = None
    bookmarks = None
    comments = None
    
    if request.user.is_authenticated():
        drafts = Story.objects.filter(status=Story.DRAFT, author=request.user)[:3]  
        bookmarks = user.stories_bookmarked.filter(status=Story.PUBLISHED)[:3]
        comments = user.user_comments.filter(name=request.user, active=True, parent=None)[:3]

    # featured = Story.objects.filter(
    #   featured=True,
    #   author=user,
    #   status=Story.PUBLISHED)

    template = 'accounts/profile.html'
    context = {
        'user': user,
        'page': 'profile',
        'is_following': is_following,
        'followings': followings,
        'latest_stories': latest_stories,
        'recommends': recommends,
        'bookmarks': bookmarks,
        'comments': comments,
    }

    return render(request, template, context)


@login_required
def comments(request, username):
    user = get_object_or_404(
        User, username=username)
    if request.user == user:
        comments = user.user_comments.filter(name=request.user, active=True, parent=None)
    else:
        raise PermissionDenied

    template = 'accounts/comments.html'
    context = {
        'user': user,
        'comments': comments,
    }

    return render(request, template, context)


@login_required
@transaction.atomic # ensure that both form classes are saved only if there is no issue with any
def settings(request, username):
    user = get_object_or_404(
        User, username=username)
    if request.user == user:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile was successully updated.')
                return HttpResponseRedirect(
                    reverse('profile', args=[username]))
            else:
                messages.error(request, 'Error updating your profile. Please correct the error below.')
        else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
    else:
        raise PermissionDenied()
    return render(
        request,
        'accounts/settings.html',
        {'user_form': user_form,
         'profile_form': profile_form})


# @ajax_required
# @require_POST
# @login_required
# def user_follow(request):
    # user_id = request.POST.get('id')
    # action = request.POST.get('action')
    # if user_id and action:
        # try:
            # user = User.objects.get(id=user_id)
            # if action == 'follow':
                # Follow.objects.get_or_create(
                    # from_user=request.user, to_user=user)
                # # from_user.profile.notify_followed(follow)
            # else:
                # Follow.objects.filter(
                    # from_user=request.user, to_user=user).delete()
                # # from_user.profile.unotify_followed(follow)
            # return JsonResponse({'status': 'ok'})
        # except User.DoesNotExist:
            # return JsonResponse({'status': 'ko'})
    # return JsonResponse({'status': 'ko'})

@login_required
def follow(request, username):
    from_user = request.user
    to_user = get_object_or_404(
        User, username=username)
    following = from_user.profile.get_following()
    current_url = request.META['HTTP_REFERER']
    if to_user not in following:
        to_follow = Follow(
            from_user=from_user, 
            to_user=to_user)
        to_follow.save()
        # from_user.profile.notify_followed(follow)
        return redirect(current_url)
    else:
        return HttpResponseBadRequest()

@login_required
def unfollow(request, username):
    from_user = request.user
    to_user = get_object_or_404(
        User, username=username)
    following = from_user.profile.get_following()
    current_url = request.META['HTTP_REFERER']
    if to_user in following:
        to_unfollow = Follow.objects.get(
            from_user=from_user, 
            to_user=to_user)
        to_unfollow.delete()
        return redirect(current_url)
    else:
        return HttpResponseBadRequest()


def following(request, username):
    user = get_object_or_404(User, username=username)
    following = user.profile.get_following()
    followers = user.profile.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True
    return render(request, 'accounts/follow.html', {
            'user': user,
            'follow_list': following,
            'is_following': is_following,
            'page': 'following',
        })


def followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.profile.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    template = 'accounts/follow.html'
    context = {
            'user': user,
            'follow_list': followers,
            'is_following': is_following,
            'page': 'followers',
    }

    return render(request, template, context)


@login_required
def notifications(request, username):
    user = get_object_or_404(User,
        username=username)
    notifications = Notification.objects.filter(to_user=request.user)

    # unread = Notification.objects.filter(to_user=request.user, is_read=False)
    # for notification in unread:
    #   notification.is_read = True
    #   notification.save()

    template = 'accounts/notifications.html'
    context = {
        'user': user,
        'notifications': notifications
    }
    
    return render(request, template, context)

# def change_friend(request, operation, pk):
#   friend = User.objects.get(pk=pk)
#   if operation == 'add':
#       Friend.make_friend(request.user, friend)
#   elif operation == 'remove':
#       Friend.lose_friend(request.user, friend)
#   return redirect('/')

#   List of all users friends.
#   friends = friends.users.all()

#   Link to remove/add friend in template
#   <a href="{% url 'accounts:change_friends' operation='remove' pk=friend.pk %}">Remove</a>
#   <a href="{% url 'accounts:change_friends' operation='add' pk=friend.pk %}">Add</a>

