from ..models import ApiKey


def get_profile(request):
    return ApiKey.objects.get(
        key=request.META['HTTP_X_DEV_API_KEY']
    ).owner
