# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 10:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import story.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='story.Comment')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('image', models.ImageField(blank=True, null=True, upload_to=story.models.story_image_path, verbose_name='image')),
                ('body', models.TextField(verbose_name='body')),
                ('status', models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='P', max_length=10, verbose_name='status')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('featured', models.BooleanField(default=False, verbose_name='featured')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('bookmarks', models.IntegerField(default=0)),
                ('favorites', models.IntegerField(default=0)),
                ('impressions', models.PositiveIntegerField(default=0, help_text='Number of page views')),
                ('read_time', models.PositiveIntegerField(default=0, help_text='Estimated time taken to read the post')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='tags.Tag')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='topics.Topic', verbose_name='topic')),
                ('users_bookmarks', models.ManyToManyField(blank=True, related_name='stories_bookmarked', to=settings.AUTH_USER_MODEL)),
                ('users_favorites', models.ManyToManyField(blank=True, related_name='stories_favorited', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Story',
                'verbose_name_plural': 'Stories',
                'ordering': ['-created'],
                'get_latest_by': 'created',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='story.Story'),
        ),
    ]
