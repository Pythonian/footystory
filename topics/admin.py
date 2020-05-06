from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ['title', 'description']
	search_fields = ['title']

