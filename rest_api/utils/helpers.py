from django.shortcuts import get_object_or_404

def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except:
        return None

def is_game_dev(request, id):
    g = get_object_or_none(Game, pk=id)
    if g:
        return g.developer == request.user.id
    return False

def forbidden_message(noun = 'authorized'):
    return 'You must be {} to perform this action'.format(noun)
    