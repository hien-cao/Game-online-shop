from ..models import ApiKey


def get_profile(request):
    """Get Profile instance from ApiKey model by `X_DEV_API_KEY` request header."""
    return ApiKey.objects.get(
        key=request.META['HTTP_X_DEV_API_KEY']
    ).owner
