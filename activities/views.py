from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Activity


User = get_user_model()


@login_required
def follow(request, username):
    from_user = request.user
    to_user = get_object_or_404(
        User, username=username)
    following = from_user.profile.get_following()
    current_url = request.META['HTTP_REFERER']
    if to_user not in following:
        activity = Activity(
            from_user=from_user, 
            to_user=to_user, 
            activity_type=Activity.FOLLOW)
        activity.save()
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
        activity = Activity.objects.get(
            from_user=from_user, 
            to_user=to_user, 
            activity_type=Activity.FOLLOW)
        activity.delete()
        return redirect(current_url)
    else:
        return HttpResponseBadRequest()
