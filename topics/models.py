from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


@python_2_unicode_compatible
class Topic(models.Model):
    title = models.CharField(
    	_('title'),
        max_length=50,
        help_text='Maximum of 50 characters.')
    slug = models.SlugField(
    	_('slug'),
    	max_length=50,
        unique=True,
        help_text='Suggested value automatically generated from the title.')
    description = models.CharField(
    	_('description'),
    	max_length=100,
    	blank=True,
        help_text='Optional description for the Category. For S.E.O purposes.')
    image = models.ImageField(
    	_('image'),
    	upload_to='topics',
    	blank=True,
    	null=True)
    likes = models.PositiveIntegerField(
        default=0, db_index=True)
    users_likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='topics_liked',
        blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'topics:detail',
            kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

    def published_story_category(self):
        """
        Returns published stories for a category instance.
        """
        return self.story_set.filter(status='P') \
                             .filter(created__lte=datetime.date.today())
