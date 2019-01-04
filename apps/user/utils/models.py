from ..models import Profile

def save_profile(backend, user, response, *args, **kwargs):
    profile = Profile(user=user)
    profile.save()
