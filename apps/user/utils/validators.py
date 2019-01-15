from ...game.models import Purchase

def is_developer(user):
    profile = user.profile
    return profile.is_developer
