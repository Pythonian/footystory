from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.urls import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from topic.models import Topic
from tag.models import Tag

from .utils import get_read_time


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
                                            .filter(status='P') \
                                            .filter(created__lte=datetime.date.today())


class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='D')


class StorySearchManager(models.Manager):
    def search(self, query):
        # qs = Story.objects.search(query)
        return self.get_queryset().filter(title__icontains=query)


def story_image_path(instance, filename):
    return 'stories/%s/%s/' % (instance.id, filename[:10])
# def story_image_path(instance, filename):
# 	return '%s/stories/%s/%s/' % (instance.author, instance.slug, filename)


class Story(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    title = models.CharField(_('title'),
                             max_length=255)
    slug = models.SlugField(_('slug'),
                            max_length=100,
                            unique=True)
    image = ProcessedImageField(upload_to=story_image_path,
                                blank=True, null=True,
                                verbose_name=_('image'),
                                processors=[ResizeToFill(750, 400)],
                                format='JPEG',
                                options={'quality': 100})
    body = models.TextField(_('body'))
    status = models.CharField(_('status'),
                              max_length=10,
                              choices=STATUS,
                              default=PUBLISHED)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name=_('stories'),
                               verbose_name=_('author'))
    created = models.DateTimeField(_('created'),
                                   auto_now_add=True)
    updated = models.DateTimeField(_('updated'),
                                   auto_now=True)
    impressions = models.PositiveIntegerField(default=0,
                                              help_text='Number of page views.')
    read_time = models.PositiveIntegerField(default=0,
                                            help_text='Estimated time taken to read the post.')
    topic = models.ForeignKey(Topic,
                              on_delete=models.CASCADE,
                              verbose_name=_('topic'),
                              blank=True,
                              null=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        help_text='Separate tags with spaces.')
    featured = models.BooleanField(
        default=False)
    favorites = models.PositiveIntegerField(default=0)
    users_favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            related_name='stories_favorited',
                                            blank=True)
    bookmarks = models.PositiveIntegerField(default=0)
    users_bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            verbose_name=_('user bookmarks'),
                                            related_name=_(
                                                'stories_bookmarked'),
                                            blank=True)
    enable_comments = models.BooleanField(
        default=True)

    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()

    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')

    def get_previous_story(self):
        return self.get_previous_by_created(status='P')

    def get_next_story(self):
        return self.get_next_by_created(status='P')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('story:detail',
                       kwargs={'username': self.author.username,
                               'slug': self.slug,
                               'id': self.id})

    def get_edit_url(self):
        return reverse('story:edit',
                       kwargs={'username': self.author.username,
                               'slug': self.slug,
                               'id': self.id})

    def get_delete_url(self):
        return reverse('story:delete',
                       kwargs={
                           'username': self.author.username,
                           'slug': self.slug,
                           'id': self.id}
                       )

    def get_feature_url(self):
        return reverse('story:feature',
                       kwargs={'id': self.id}
                       )

    def get_summary(self):
        if len(self.body) > 140:
            return '{0}...'.format(self.body[:140])
        else:
            return self.body

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.body:
            # Get the contents in the body and set it to html_string
            html_string = self.body
            # Calculate the read time from the returned html_string
            read_time_var = get_read_time(html_string)
            # Pass the value to the read_time field
            self.read_time = read_time_var

        # When a story has been featured, update the
        # other existing featured story as False
        if self.featured:
            story_list = Story.objects.filter(featured=True).exclude(pk=self.pk)
            if story_list.exists():
                story_list.update(featured=False)

        super(Story, self).save(*args, **kwargs)
        # Ping google due to sitemap changes that
        # arises from a new Post being created.
        try:
            ping_google()
        except Exception:
            pass

    # def create_tags(self, tags):
    # 	tags = tags.strip()
    # 	tag_list = tags.split(' ')
    # 	for tag in tag_list:
    # 		if tag:
    # 			t, created = Tag.objects.get_or_create(
    # 				name=tag.lower(), story=self)

    @property
    def get_tags(self):
        return [t for t in self.tags.all()]
    # def get_tags(self):
    #     return ', '.join([t.title for t in self.tags.all()[:3]])
    # get_tags.short_description = 'Tags'

    @staticmethod
    def get_published_stories():
        stories = Story.objects.filter(status=Story.PUBLISHED)
        return stories

    def get_comments(self):
        return Comment.objects.filter(story=self, active=True, parent=None)

    def get_last_ten_stories(self):
        return self.story.order_by('-created')[:10]

    @property
    def word_count(self):
        return len(strip_tags(self.body).split())


class Comment(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='comments')
    name = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_comments')
    body = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True)
    active = models.BooleanField(
        default=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    class Meta:
        ordering = ['-created']

    def children(self):
        # Get the replies of each comment
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def __str__(self):
        return f'{self.name.username} - {self.story.title}'

# class EditHistory(models.Model):
# 	"""Model to track the Edit History of a Story."""
# 	story = models.ForeignKey(
# 		Story)
# 	editor = models.ForeignKey(
# 		settings.AUTH_USER_MODEL)
# 	edited_on = models.DateTimeField(
# 		auto_now_add=True)
# 	summary = models.CharField(
# 		max_length=200,
# 		blank=True,
# 		help_text='Optional Summary of what you edited.')

# 	class Meta:
# 		ordering = ['-edited_on']
# 		verbose_name_plural = 'Edit Histories'

# 	def __str__(self):
# 		return "{} edited their story {}".format(
# 			self.editor, self.story.title)

# 17th November 2016 - Seyi Pythonian
