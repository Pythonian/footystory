from django import template
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def get_followers_count(username):
	user = get_object_or_404(
		User, username=username)
	return user.profile.get_followers_count()


@register.simple_tag
def get_following_count(username):
	user = get_object_or_404(
		User, username=username)
	return user.profile.get_following_count()


@register.simple_tag
def is_user_following(request, username):
	user = get_object_or_404(
		User, username=username)
	followers = user.profile.get_followers()
	is_following = False
	if request.user in followers:
		is_following = True
	return is_following
