from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from ..user.utils.validators import is_developer
from .forms.add_game import AddGameForm

from .models import Game

# Add game
# TODO Change redirection to profile/settings?
@login_required
@user_passes_test(is_developer, login_url='/games/library/')
def add_game(request, *args, **kwargs):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddGameForm(request.POST)
        # is form valid:
        if form.is_valid():
            # TODO Store to DB.
            data = form.cleaned_data
            game = Game(
                name=data['name'],
                description=data['description'],
                url=data['url'],
                price=data['price'],
                created_by=request.user.profile
            )
            game.save()
            # redirect to a games uploaded by user:
            return HttpResponseRedirect('/games/my/')

    # if a GET (or any other method), form instance is blank
    else:
        form = AddGameForm()

    return render(request, 'add_game.html', { 'form': form })

# GET: Display games view
# POST: Add game
def games(request, *args, **kwargs):
    if (request.method == 'GET'):
        latest_games = Game.objects.order_by('created_at')[:5]
        print(latest_games)
        # TODO Render
        context = {
            'latest': latest_games,
            'games': 'is-active',
        }
        return render(request, 'games.html', context)
    if (request.method == 'POST'):
        return add_game(request, *args, **kwargs)

# GET: Display games purchased
@login_required
def library(request, *args, **kwargs):
    profile = request.user.profile
    games = profile.games
    print(games)
    context = {
        'library': 'is-active',
    }
    return HttpResponse('List games I have purchased!')

# GET: Display games uploaded
@login_required
@user_passes_test(is_developer, login_url='/games/library')
def my(request, *args, **kwargs):
    profile = request.user.profile
    games = Game.objects.filter(created_by=request.user.profile)
    print(games)
    context = {
        'my': 'is-active',
    }
    return HttpResponse('List games uploaded by me!')

def play(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    print(game)
    return HttpResponse('Hello from game play view!')
