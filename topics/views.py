from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from story.models import Story
from account.decorators import ajax_required

User = get_user_model()


def list(request):
	# topics = Topic.objects.exclude(
	# 	users_likes=request.user)
	topics = Topic.objects.all()
    user_topics = None

    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        user_topics = user.topics_liked.all()
	return render(request,
		'topics/list.html',
		{'section': 'topic',
		'topics': topics,
		'user_topics': user_topics})

@login_required
def user_topics(request):
	user = get_object_or_404(User,
		username=request.user.username)
	topics = user.topics_liked.all()
	return render(request,
		'topics/user_topics.html',
		{'user': user,
		'topics': topics})

def detail(request, slug):
	topic = get_object_or_404(Topic,
		slug=slug)
	stories = topic.story_set.filter(status=Story.PUBLISHED)
	# stories = topic.story_set.all()

	return render(request,
		'topics/detail.html',
		{'topic': topic,
		'stories': stories})

@login_required
def like(request, id):
	topic = get_object_or_404(Topic,
		id=id)
	current_url = request.META['HTTP_REFERER']
	users_likes = topic.users_likes.filter(
		username=request.user.username)
	if not users_likes:
		topic.likes += 1
		topic.users_likes.add(request.user)
		messages.success(request, "You've liked this topic.")
		return redirect(current_url)
	else:
		return HttpResponseBadRequest()

# @ajax_required
# @login_required
# @require_POST
# def topic_like(request):
#     topic_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if topic_id and action:
#         try:
#             topic = Topic.objects.get(id=topic_id)
#             if action == 'like':
#                 topic.users_like.add(request.user)
#             else:
#                 topic.users_like.remove(request.user)
#             return JsonResponse({'status': 'ok'})
#         except:
#             pass
#     return JsonResponse({'status': 'ko'})

@login_required
def unlike(request, id):
	topic = get_object_or_404(Topic,
		id=id)
	current_url = request.META['HTTP_REFERER']
	users_likes = topic.users_likes.filter(
		username=request.user.username)
	if users_likes:
		topic.likes -= 1
		topic.users_likes.remove(request.user)
		messages.success(request, "You've unliked this topic.")
		return redirect(current_url)
	else:
		return HttpResponseBadRequest()
