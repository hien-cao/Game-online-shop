import json
from functools import wraps
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from ..models import ApiKey
from ....user.utils.validators import api_request_is_developer


def json_response(fn):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = fn(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = objects
            if request.GET.get("callback") is not None:
                # a jsonp response!
                data = '{0}({1});'.format(request.GET.get('callback'), data)
                return HttpResponse(data, "text/javascript")
            elif objects['content'] is None:
                raise
            else:
                return JsonResponse(data, status=200)
        except:  # noqa: E722
            return JsonResponse(data, status=400)
    return decorator


def validate_request(fn):
    def decorator(request, *args, **kwargs):
        error_response = None
        # TODO: Response that only https allowed
        if settings.ENVIRONMENT == 'production' and not request.is_secure():
            error_response = JsonResponse(
                {'message': 'Invalid request protocol'},
                status=403
            )
        if request.method != "GET":
            error_response = JsonResponse(
                {'message': 'Invalid request method'},
                status=403
            )
        elif not request.META['HTTP_X_DEV_API_KEY']:
            error_response = JsonResponse(
                {'message': 'Missing required header: X-DEV-API-KEY'},
                status=403
            )
        elif ApiKey.objects.filter(key=request.META['HTTP_X_DEV_API_KEY']) \
                .count() == 0:
            error_response = JsonResponse(
                {'message': 'Invalid api key'},
                status=403
            )
        return fn(request, *args, **kwargs, error_response=error_response)
    return decorator


def passes_test(test_fn):
    def decorator(fn):
        @wraps(fn)
        def _wrapped_view(request, *args, **kwargs):
            if test_fn(request):
                return fn(request, *args, **kwargs)
            return JsonResponse({'message': 'Invalid request.'}, status=403)
        return _wrapped_view
    return decorator


def dev_api_request(fn):
    """
    Wrapper decorator for all most common decorators
    in dev api requests.
    - json_response
    - passes_test(api_request_is_developer)
    - validate_request
    """
    @json_response
    @passes_test(api_request_is_developer)
    @validate_request
    def decorator(request, *args, **kwargs):
        return fn(request, *args, **kwargs)
    return decorator
