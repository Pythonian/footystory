from django.shortcuts import render, redirect, get_object_or_404
from .models import Story, Comment
from .forms import StoryForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from .decorators import ajax_required
from tags.models import Tag
#from activities.models import Activity

User = get_user_model()


@login_required
def create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            status = form.cleaned_data.get('status')
            if status in [Story.PUBLISHED, Story.DRAFT]:
                story.status = form.cleaned_data.get('status')
            story.save()
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(title=tag_name.lower())
                story.tags.add(tag)
            return redirect(story.get_absolute_url())
		else:
            messages.warning(
                request, "There was an error while trying to save your story, please check below.")
    else:
        form = StoryForm()

    template = 'story/form.html'
    context = {
        'form': form,
        'create': True
    }

    return render(request, template, context)


def detail(request, username, slug, id):
    user = get_object_or_404(User,
                             username=username)
    if user == request.user:
        story = get_object_or_404(
            Story,
            author__username=username,
            slug__iexact=slug,
            id=id)
    else:
        story = get_object_or_404(
            Story,
            author__username=username,
            slug__iexact=slug,
            id=id,
            status=Story.PUBLISHED)

    followers = user.profile.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    # Create a session key for a user to monitor viewed story
    session_key = 'viewed_story_{}'.format(story.pk)
    if not request.session.get(session_key, False):
        story.impressions += 1
        story.save()
        request.session[session_key] = True

    # Comments
    comments = story.get_comments()
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.name = request.user
        new_comment.story = story

        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment.parent = parent_obj
        new_comment.save()
        request.user.profile.notify_commented(story)
        request.user.profile.notify_also_commented(story)

        messages.success(request, 'Your comment has been successfully posted.')
        return redirect(story)

    template = 'story/detail.html'
    context = {
        'story': story,
        'comments': comments,
        'form': form,
        'user': user,
        'is_following': is_following,
        'related_stories': True,
    }

    return render(request, template, context)

# @login_required
# @ajax_required
# def comment(request):
# 	try:
# 		if request.method == 'POST':
# 			story_id = request.POST.get('story')
# 			story = Story.published.get(pk=story_id)
# 			comment = request.POST.get('comment')
# 			comment = comment.strip()
# 			if len(comment) > 0:
# 				story_comment = Comment(name=request.user, story=story, comment=comment)
# 				story_comment.save()
# 			html = ''
# 			for comment in story.get_comments():
# 				html = '{0}{1}'.format(html, render_to_string(
# 					'articles/partial_article_comment.html',
# 					{'comment': comment}))

# 			return HttpResponse(html)

# 		else:
# 			return HttpResponseBadRequest()

# 	except Exception:
# 		return HttpResponseBadRequest()


def list(request, username):
    user = get_object_or_404(User,
                             username=username)
    stories = Story.published.filter(author=user)

    template = 'story/list.html'
    context = {
        'user': user,
        'page': 'list',
        'stories': stories
    }

    return render(request, template, context)


def drafts(request, username):
    user = get_object_or_404(User,
                             username=username)
    if user == request.user:
        stories = Story.draft.filter(author=request.user)
    else:
        raise PermissionDenied()

    template = 'story/drafts.html'
    context = {
        'user': user,
        'stories': stories,
    }

    return render(request, template, context)


@login_required
def bookmarks(request, username):
    user = get_object_or_404(User,
                             username=username)
    if user == request.user:
        stories = user.stories_bookmarked.filter(status=Story.PUBLISHED)
    else:
        raise PermissionDenied()

    template = 'story/bookmarks.html'
    context = {
        'user': user,
        'stories': stories
    }

    return render(request, template, context)


def favorites(request, username):
    user = get_object_or_404(User,
                             username=username)
    stories = user.stories_favorited.filter(status=Story.PUBLISHED)

    template = 'story/favorites.html'
    context = {
        'user': user,
        'stories': stories
    }

    return render(request, template, context)


@login_required
def edit(request, username, slug, id):
    user = get_object_or_404(
        User, username=username)
    story = get_object_or_404(
        Story,
        author__username=user,
        slug__iexact=slug,
        id=id)
    tags = ''
    for tag in story.get_tags:
        tags = '{0} {1}'.format(tags, tag.title)
    tags = tags.strip()
    if story.author == user:
        if request.method == 'POST':
            form = StoryForm(request.POST, request.FILES, instance=story)
            if form.is_valid():
                edited_story = form.save(commit=False)
                edited_story.created = timezone.now()
                edited_story.save()
                messages.success(
                    request, "Your story was successfully edited.")
                return redirect(edited_story.get_absolute_url())
            else:
                messages.error(
                    request, "Failed! There was a problem while editing your story.")
        else:
            form = StoryForm(instance=story, initial={'tags': tags})
            # form = StoryForm(instance=story)
    else:
        raise PermissionDenied()

    template = 'story/form.html'
    context = {
        'form': form,
        'user': user,
        'story': story
    }

    return render(request, template, context)


@login_required
def delete(request, username, slug, id):
    user = get_object_or_404(
        User, username=username)
    story = get_object_or_404(
        Story,
        author__username=user,
        slug__iexact=slug,
        id=id)
    if story.author == request.user:
        if request.method == 'POST':
            story.delete()
            messages.success(
                request, "Your story has been successfully deleted.")
            return redirect('story:list', username=story.author.username)
        return render(request,
                      'story/delete.html',
                      {'story': story})
    else:
        raise PermissionDenied()


@login_required
def feature(request, id):
    story = get_object_or_404(
        Story,
        id=id)
    current_url = request.META['HTTP_REFERER']
    if story.author == request.user:
        story.featured = True
        story.save()
        return redirect(current_url)
    else:
        raise PermissionDenied()


@login_required
def favorite(request, id):
    story = get_object_or_404(
        Story,
        id=id)
    current_url = request.META['HTTP_REFERER']
    users_favorites = story.users_favorites.filter(
        username=request.user.username)
    if not users_favorites:
        story.favorites += 1
        story.users_favorites.add(request.user)
        request.user.profile.notify_favorited(story)
        messages.success(
            request, "This story has been added to your favorites.")
        return redirect(current_url)
    else:
        return HttpResponseBadRequest()


@login_required
def unfavorite(request, id):
    story = get_object_or_404(
        Story,
        id=id)
    current_url = request.META['HTTP_REFERER']
    users_favorites = story.users_favorites.filter(
        username=request.user.username)
    if users_favorites:
        story.favorites -= 1
        story.users_favorites.remove(request.user)
        request.user.profile.unnotify_favorited(story)
        messages.success(
            request, "This story has been deleted from your favorites.")
        return redirect(current_url)
    else:
        return HttpResponseBadRequest()


@login_required
def add_bookmark(request, id):
    story = get_object_or_404(
        Story,
        id=id)
    current_url = request.META['HTTP_REFERER']
    users_bookmarks = story.users_bookmarks.filter(
        username=request.user.username)
    if not users_bookmarks:
        story.bookmarks += 1
        story.users_bookmarks.add(request.user)
        messages.success(
            request, "This story has been added to your bookmarks.")
        return redirect(current_url)
    else:
        return HttpResponseBadRequest()


@login_required
def delete_bookmark(request, id):
    story = get_object_or_404(
        Story,
        id=id)
    current_url = request.META['HTTP_REFERER']
    users_bookmarks = story.users_bookmarks.filter(
        username=request.user.username)
    if users_bookmarks:
        story.bookmarks -= 1
        story.users_bookmarks.remove(request.user)
        messages.success(
            request, "This story has been deleted from your bookmarks.")
        return redirect(current_url)
    else:
        return HttpResponseBadRequest()


# @login_required
# @ajax_required
# def favorite(request):
#     question_id = request.POST['question']
#     question = Question.objects.get(pk=question_id)
#     user = request.user
#     activity = Activity.objects.filter(activity_type=Activity.FAVORITE,
#                                        user=user, question=question_id)
#     if activity:
#         activity.delete()
#         user.profile.unotify_favorited(question)
#     else:
#         activity = Activity(activity_type=Activity.FAVORITE, user=user,
#                             question=question_id)
#         activity.save()
#         user.profile.notify_favorited(question)

#     return HttpResponse(question.calculate_favorites())


# @login_required
# def recommend(request, username, slug, id):
# 	story = get_object_or_404(
# 		Story,
# 		author__username=username,
# 		slug__iexact=slug,
# 		id=id)
# 	user = request.user
# 	recommends = story.get_recommends()
# 	current_url = request.META['HTTP_REFERER']
# 	if recommend not in recommends:
# 		activity = Activity(
# 			activity_type=Activity.RECOMMEND,
# 			user=user,
# 			story=story.id)
# 		activity.save()
# 		return redirect(current_url)
# 	else:
# 		return HttpResponseBadRequest()

    # if activity:
    # 	activity.delete()
    # 	return redirect(current_url)
    # else:
    # 	activity = Activity(activity_type=Activity.RECOMMEND,
    # 		user=user, story=story.id)
    # 	activity.save()
    # 	return redirect(current_url)
# def image_like(request):
# 	# id of the image on which the action is performed
# 	image_id = request.POST.get('id')
# 	# the action the user wants to perform: 'like' or 'unlike'
# 	action = request.POST.get('action')
# 	if image_id and action:
# 		try:
# 			image = Image.objects.get(id=image_id)
# 			if action == 'like':
# 				image.users_like.add(request.user)
# 				create_action(request.user, 'likes', image)
# 			else:
# 				image.users_like.remove(request.user)
# 			return JsonResponse({'status': 'ok'})
# 		except:
# 			pass
# 	return JsonResponse({'status': 'ko'})
