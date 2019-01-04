from ..models import Profile

def is_developer(user):
    profile = Profile.objects.get(user=user)
    print(profile.is_developer)
    return profile.is_developer
