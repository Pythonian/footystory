from django.shortcuts import redirect
from django.http import HttpResponseBadRequest


def is_anonymous_user(request):
    if request.user.is_anonymous:
        return request
    return redirect('home')


def anonymous_required(func):
    def wrapped_func(request, *args, **kwargs):
        request = is_anonymous_user(request)
        resp = func(request, *args, **kwargs)
        return resp
    return wrapped_func

# Return an HTTP 400 code if the request is not Ajax
def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
