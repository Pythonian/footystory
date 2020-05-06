from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _ 
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User

from notifications.models import Notification

def user_avatar_path(instance, filename):
	return '%s/avatars/%s/' % (instance.user.username, filename)


class Profile(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		verbose_name=_('user'),
	)
	about = models.CharField(
		_('about'),
		blank=True,
		max_length=140,
		help_text=_('Tell us about yourself in 140 characters.'),
	)
	avatar = ProcessedImageField(
		upload_to=user_avatar_path,
		blank=True,
		null=True,
		verbose_name=_('avatar'),
		processors = [ResizeToFill(70, 70)],
		format = 'JPEG',
		options = {'quality': 100})
	email_confirmed = models.BooleanField(
		_('email confirmed?'),
		default=False,
		help_text="Determine if the User's email has been confirmed.",
	)
	verified_account = models.BooleanField(
		_('verified account?'),
		default=False,
	)
	website = models.URLField(
		_('website'),
		blank=True,
		null=True,
		help_text=_('Begin your URL with http:// or https://'),
	)
	location = models.CharField(
		_('location'),
		max_length=30,
		blank=True,
		null=True,
	)
	favorite_club = models.CharField(
		_('favorite club'),
		max_length=40,
		blank=True,
		null=True,
	)


	class Meta:
		verbose_name = _('Profile')
		verbose_name_plural = _('Profiles')

	def __str__(self):
		return self.user.username

	def get_website(self):
		website = self.website
		if "http://" not in self.website and "https://" not in self.website:
			website = "http://" + str(self.website)
		return website

	def get_screen_name(self):
		try:
			if self.user.get_full_name():
				return self.user.get_full_name()
			else:
				return self.user.username
		except:
			return self.user.username

    # def get_picture(self):
    #     no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
    #     try:
    #         filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
    #             self.user.username + '.jpg'
    #         picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
    #             self.user.username + '.jpg'
    #         if os.path.isfile(filename):  # pragma: no cover
    #             return picture_url
    #         else:  # pragma: no cover
    #             gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
    #                 hashlib.md5(self.user.email.lower()).hexdigest(),
    #                 urllib.urlencode({'d': no_picture, 's': '256'})
    #                 )
    #             return gravatar_url

    #     except Exception:
    #         return no_picture

	def get_summary(self):
		if len(self.body) > 140:
			return '{0}...'.format(
				self.body[:140])
		else:
			return self.body


	# def get_avatar(self):
	# 	avatar = settings.MEDIA_ROOT + '/default/' + 'avatar.PNG'
		# if not self.avatar: # footystory/images/avatar.png
		# 	# avatar = settings.STATIC_ROOT + '/footystory/images/avatar.png'
		# 	avatar = settings.MEDIA_ROOT + '/default/' + 'avatar.png'
		# else:
		# 	return avatar

	def get_about(self):
		about = self.about
		if len(self.about) > 70:
			return '{0}...'.format(
				self.about[:70])
		date_joined = self.user.date_joined.strftime("%B %Y")
		if not self.about:
			about = "Joined Footystory since <span class='primary'>{0}</span> and a fan of <span class='primary'>{1}</span>.".format(
				date_joined, self.favorite_club)
		return about

	def get_followers(self):
		to_followers = Follow.objects.filter(to_user__pk=self.pk)
		followers = []
		for to_follower in to_followers:
		    followers.append(to_follower.from_user)
		return followers

	def get_followers_count(self):
	    followers_count = Follow.objects.filter(to_user__pk=self.pk).count()
	    return followers_count

	def get_following(self):
	    to_followings = Follow.objects.filter(from_user__pk=self.pk)
	    following = []
	    for to_following in to_followings:
	        following.append(to_following.to_user)
	    return following

	def get_following_count(self):
	    following_count = Follow.objects.filter(from_user__pk=self.pk).count()
	    return following_count

	def notify_commented(self, story):
		# Check if the User who commented is not the same as the Author of the story
		if self.user != story.author:
			Notification(notification_type=Notification.COMMENTED, 
				from_user=self.user, 
				to_user=story.author, 
				story=story).save()

	def notify_also_commented(self, story):
		comments = story.get_comments()
		users = []
		for comment in comments:
			if comment.name != self.user and comment.name != story.author:
				users.append(comment.name.pk)
		users = list(set(users))
		for user in users:
			Notification(notification_type=Notification.ALSO_COMMENTED,
				from_user=self.user,
				to_user=User(id=user),
				story=story).save()

	def notify_followed(self, follow):
		if self.user != follow.to_user:
			Notification(notification_type=Notification.FOLLOWED,
				from_user=self.user,
				to_user=follow.to_user,
				follow=follow).save()

	def notify_favorited(self, story):
		if self.user != story.author:
			Notification(notification_type=Notification.FAVORITED, 
				from_user=self.user, 
				to_user=story.author, 
				story=story).save()

	def unnotify_favorited(self, story):
		if self.user != story.author:
			Notification.objects.filter(
				notification_type=Notification.FAVORITED,
				from_user=self.user,
				to_user=story.author,
				story=story).delete()


class Follow(models.Model):
	from_user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='follower')
	to_user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='following')
	created = models.DateTimeField(
		auto_now_add=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return f"{self.from_user.username} follows {self.to_user.username}"


# class Friend(models.Model):
# 	users = models.ManyToManyField(
# 		settings.AUTH_USER_MODEL)
# 	current_user = models.ForeignKey(
# 		settings.AUTH_USER_MODEL,
# 		related_name='owner',
# 		null=True)

# 	@classmethod
# 	def make_friend(cls, current_user, new_friend):
# 		friend, created = cls.objects.get_or_create(
# 			current_user=current_user)
# 		friend.users.add(new_friend)

# 	@classmethod
# 	def lose_friend(cls, current_user, new_friend):
# 		friend, created = cls.objects.get_or_create(
# 			current_user=current_user)
# 		friend.users.remove(new_friend)