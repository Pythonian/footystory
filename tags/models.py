from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
# from story.models import Story


class Tag(models.Model):
    title = models.CharField(
        _('title'),
        max_length=10)
    slug = models.SlugField(
        _('slug'),
        max_length=10,
        help_text='Suggested value automatically generated from the title.')
    created = models.DateTimeField(
        _('created'),
        auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tags:detail', kwargs={'slug': self.slug})

    # @staticmethod
    # def get_popular_tags():
    #   tags = Tag.objects.all()
    #   count = {}
    #   for tag in tags:
    #       if tag.story.status == Story.PUBLISHED:
    #           if tag.title in count:
    #               count[tag.title] = count[tag.title] + 1
    #           else:
    #               count[tag.title] = 1
    #   sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
    #   return sorted_count[:20]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def published_stories_tag(self):
        """
        Returns published stories for a tag instance.
        """
        return self.story_set.filter(status='P').filter(
            created__lte=datetime.date.today())
