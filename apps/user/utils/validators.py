from ...apis.dev_api.models import ApiKey


def is_developer(user):
    return user.profile.is_developer


def api_request_is_developer(request):
    try:
        api_key = ApiKey.objects.get(key=request.META['HTTP_X_DEV_API_KEY'])
        return api_key.owner.is_developer
    except: # noqa E722
        return False
