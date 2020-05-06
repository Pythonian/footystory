from django.db import models
from django.conf import settings


class Activity(models.Model):
	BOOKMARK = 'B'
	RECOMMEND = 'R'
	ACTIVITY_TYPES = (
		(BOOKMARK, 'Bookmark'),
		(RECOMMEND, 'Recommend'),
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL)
	activity_type = models.CharField(
		max_length=1, 
		choices=ACTIVITY_TYPES)
	story = models.IntegerField(
		null=True,
		blank=True)
	created = models.DateTimeField(
		auto_now_add=True)

	class Meta:
		ordering = ['-created']

	class Meta:
		verbose_name = 'Activity'
		verbose_name_plural = 'Activities'

	def __str__(self):
		return self.activity_type
