from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from story.models import Story
from topics.models import Topic 

User = get_user_model()


def home(request):
	following_stories = None
	recommended_stories = None
	user_topics_stories = None
	if request.user.is_authenticated:
		# Latest stories on the Site
		stories = Story.published.all()[:3]

		# Stories published by authors the user is following
		following_stories = Story.published.filter(
			author__in=request.user.profile.get_following())[:6]

		# Stories recommended by a User's following.
		# Exclude recommended stories published by the User.
		recommended_stories = Story.published.filter(
			users_favorites__in=request.user.profile.get_following()).exclude(author=request.user)[:6]

		# Stories from the topics a User Liked.
		# Exclude stories published by the User in this category
		user_topics_stories =  Story.published.filter(
			topic__in=request.user.topics_liked.all()).exclude(author=request.user)[:6]

		# Suggest topics for a User to Like excluding the already Liked ones
		suggested_topics = Topic.objects.exclude(users_likes=request.user)[:4]


		# Get names of those who recommended the story {{ story.users_favorites.all }}
		# Get the list of the stories
		# for story in recommended_stories:
		# 	# Get the list of users who recommended the story
		# 	for recommender in story.users_favorites.all():
		# 		if recommender in request.user.profile.get_following():
		# 			print(story.title, recommender.profile.get_screen_name())
	else:
		# Latest stories on the Site
		stories = Story.published.all()[:6]
		# Suggest topics for Anonymous user to visit
		suggested_topics = Topic.objects.all()[:4]


	template = 'site/home.html'
	context = {
		'section': 'home',
		'stories': stories,
		'following_stories': following_stories,
		'recommended_stories': recommended_stories,
		'user_topics_stories': user_topics_stories,
		'topics': suggested_topics,
	}
	
	return render(request, template, context)


def people(request):
	if request.user.is_authenticated:
		users = User.objects.exclude(
			username=request.user).exclude(
			is_active=False)
	else:
		users = User.objects.exclude(
			is_active=False)

	template = 'site/people.html'
	context = {
		'section': 'people',
		'users': users
	}

	return render(request, template, context)

# def people(request):
# 	if request.user.is_authenticated:
# 		# Recommend people to a User based on mutual favorite club.
# 		# Get the name of User's favorite club
# 		user_favorite_club = request.user.profile.favorite_club
# 		# Split the club name into a list and pick first item
# 		club_name = user_favorite_club.split()[0]
# 		# Get lists of users who also supports the User's favorite club
# 		# Exclude both the current User and inactive users.
# 		users = User.objects.filter(
# 			profile__favorite_club__icontains=club_name).exclude(
# 			username=request.user).exclude(
# 			is_active=False)
# 	else:
# 		users = User.objects.exclude(
# 			is_active=False)

# 	template = 'site/people.html'
# 	context = {
# 		'section': 'people',
# 		'users': users
# 	}

# 	return render(request, template, context)


def stories(request):
	user = request.user
	if request.user.is_authenticated:
		# Stories published by a user
		user_stories = Story.published.filter(
			author=request.user)
		# Stories published by authors the user is following
		following_stories = Story.published.filter(
			author__in=user.profile.get_following())
		# Join the querysets together into a single queryset
		stories = (user_stories | following_stories).distinct()

		# Stories related to the club the user supports via Tags.
		# Get the name of the club
		# user_club = request.user.profile.favorite_club
		# user_club_stories = Story.published.filter(
			# topic__title__in=user_club)
	else:
		stories = Story.published.all()

	template = 'site/stories.html'
	context = {
		'stories': stories,
	}

	return render(request, template, context)
