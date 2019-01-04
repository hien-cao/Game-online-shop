from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse

from ..user.utils.validators import is_developer

# Add game
@user_passes_test(is_developer)
@login_required(login_url='/login/')
def add_game(request, *args, **kwargs):
    # TODO: Game add logic
    return HttpResponse('Game successfully added!')

# GET: Display games view
# POST: Add game
def games(request, *args, **kwargs):
    if (request.method == 'GET'):
        return HttpResponse('Hello from games!')
    if (request.method == 'POST'):
        return add_game(request, *args, **kwargs)

# GET: Display games purchased
@login_required
def library(requst, *args, **kwargs):
    return HttpResponse('List my games!')

@user_passes_test(is_developer, login_url='/games/library')
@login_required
def my(request, *args, **kwargs):
    return HttpResponse('List games uploaded by me!')

