from ..models import Profile

def save_profile(backend, user, response, *args, **kwargs):
    if user.profile == None:
        profile = Profile(user=user)
        profile.save()
