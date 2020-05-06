from django.contrib import admin
from .models import Story, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    classes = ['collapse']
    exclude = ['parent']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created']
    list_filter = ['created']
    search_fields = ['title', 'author__username', 'body']
    date_hierarchy = 'created'
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]
