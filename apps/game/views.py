import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from ..user.utils.validators import is_developer
from .forms.add_game import AddGameForm

from .models import Game, Purchase, Highscore
from .contexts import (
    games_context,
    library_context,
    my_context,
    get_play_game_context
)

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
            return HttpResponseRedirect('/games/uploads/')

    # if a GET (or any other method), form instance is blank
    else:
        form = AddGameForm()

    return render(request, 'add_game.html', {'form': form})

# GET: Display games view
# POST: Add game
def games(request, *args, **kwargs):
    if request.method == 'GET':
        latest_games = Game.objects.order_by('created_at')[:5]
        print(latest_games)
        context = {
            'latest': latest_games,
            **games_context,
        }
        return render(request, 'games.html', context)
    if request.method == 'POST':
        return add_game(request, *args, **kwargs)
    return HttpResponse(status=404)

# GET: Display single game view
# POST: Add game
def game_details(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'GET':
        purchased = bool(Purchase.objects.filter(game=game_id, created_by=request.user.id, purchased_at__isnull=False))
        if request.user.is_authenticated:
            if game.created_by.user.id == request.user.id:
                # TODO Render (and return) developer view
                pass
        return render(request, 'game_details.html', {'game': game, 'purchased': purchased})

    return HttpResponse(status=404) # other methods not supported


@login_required
def purchase_game(request, game_id):
    if request.method != 'GET': # Only supports get -method
        return HttpResponse(status=404)
    # Should redirect to game page if already purchased
    if bool(Purchase.objects.filter(game=game_id, created_by=request.user.id, purchased_at__isnull=False)):
        return HttpResponseRedirect('/games/{}'.format(game_id))

    # Handles the activation of purchase here
    if request.GET.get('result') == 'success':
        Purchase.activate(request.GET)
        return HttpResponseRedirect('/games/{}'.format(game_id))
    if request.GET.get('result') == 'cancel':
        return HttpResponseRedirect('/games/{}'.format(game_id))
    # Were not raising errors at this point (if they can be even happen).
    # Invalid payment information gives an error message when accessing the payment platform

    game = get_object_or_404(Game, pk=game_id)

    purchase = Purchase(
        game=game,
        created_by=request.user.profile,
    )
    purchase.save()

    return render(request, 'purchase.html', {
        **purchase.get_payment_context(),
        'purchase': purchase,
        'success_url': '{}?purchase_id={}'.format(request.build_absolute_uri('?'), purchase.id),
        'error_url': '{}?purchase_id={}'.format(request.build_absolute_uri('?'), purchase.id),
        'cancel_url': '{}?purchase_id={}'.format(request.build_absolute_uri('?'), purchase.id),
    })


# GET: Display games purchased
@login_required
def library(request, *args, **kwargs):
    profile = request.user.profile
    purchases = profile.games
    print(games)
    context = {
        **library_context,
    }
    return HttpResponse('List games I have purchased!')

# GET: Display games uploaded
@login_required
@user_passes_test(is_developer, login_url='/games/library')
def uploads(request, *args, **kwargs):
    profile = request.user.profile
    games = Game.objects.filter(created_by=request.user.profile)
    print(games)
    context = {
        **my_context,
    }
    return HttpResponse('List games uploaded by me!')

# GET: Display games uploaded
@login_required
def play(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    profile = request.user.profile
    if profile.games and Purchase.objects.filter(created_by=profile, game=game).count() > 0:
        print('User has purchased the game')
        context = {
            'profile': profile,
            **get_play_game_context(game)
        }
        print(context)
        return render(request, 'play_game.html', context)

    print('User has not purchased the game.')
    # TODO Redirect to purchase.
    return HttpResponseRedirect('games')

# POST: Store a highscore
@login_required
def save_score(request, game_id):
    """
    NOTE: It is not possible to make a cheatproof highscore storage
    as the game state is maintained in the client and not on the server.

    Hence, there is no "secret keys" or any other redurdant variables
    that would try to abstract the storing of scores in such way that
    an adversary (client) could not find a way to store whatever scores they wished.
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        score = body['score']
        game = get_object_or_404(Game, pk=game_id)
        highscore = Highscore(
            score=score,
            game=game,
            created_by=request.user.profile
        )
        save_response = highscore.save()
        return JsonResponse(save_response)
    return JsonResponse({"message": "invalid request!"})
