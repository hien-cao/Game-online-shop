from django.http import HttpResponseForbidden
from .helpers import forbidden_message

def dev(fn):
    def decorator(request, *args, **kwargs):
        try:
            assert request.user.is_developer == True
            return fn(request, *args, **kwargs)
        except:
            raise HttpResponseForbidden(
                forbidden_message('a developer')
            )
    return decorator
