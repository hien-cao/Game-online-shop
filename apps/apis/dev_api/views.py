from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import ApiKey


def _generate(profile):
    instance = ApiKey.objects.create(owner=profile)
    instance.save()
    return JsonResponse({"message": instance.key})


def generate(request):
    if request.method == 'POST' and request.user.profile.is_developer:
        try:
            existing_key = ApiKey.objects.get(owner=request.user.profile)
            existing_key.delete()
            return _generate(request.user.profile)
        except ObjectDoesNotExist:
            return _generate(request.user.profile)

    return HttpResponse(status=404)
