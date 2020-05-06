from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Story

# Return an HTTP 400 code if the request is not Ajax
def ajax_required(f):
	def wrap(request, *args, **kwargs):
		if not request.is_ajax():
			return HttpResponseBadRequest()
		return f(request, *args, **kwargs)
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap
	
def user_is_story_author(function):
    '''
    This checks to make sure only the Author of the story
    can either edit or delete his story.
            request.user == story.author
    '''
    def wrap(request, year, month, day, slug, *args, **kwargs):
        story = get_object_or_404(
            Story,
            slug__iexact=slug,
            created__year=year,
            created__month=month,
            created__day=day)
        if story.author == request.user:
            request.story = story
            return function(request, year, month, day, slug, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
