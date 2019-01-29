import json
import base64
import re
import pytz
from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
    JsonResponse
)

from ..user.utils.validators import is_developer
from .forms.game_form import GameForm

from .models import Game, Purchase, Highscore, Tag, Save
from .contexts import (
    games_context,
    library_context,
    uploads_context,
    get_play_game_context,
    get_upsert_game_context,
    get_purchase_context,
)


def parse_tags(description):
    regex = re.compile(r'\B#\w+')
    return regex.findall(description)


# Create new tags from game's description
def create_tags(description):
    parsed_tags = parse_tags(description)
    tags = []
    if parsed_tags != []:
        for tag_name in parsed_tags:
            obj, _ = Tag.objects.get_or_create(name=tag_name.lower())
            tags.append(obj)
    return tags


# Add/Edit game
# TODO Change redirection to profile/settings?


@login_required
@user_passes_test(is_developer, login_url='/games/library/')
def manage_game(request, game_id=None):
    if game_id:
        url = 'edit_game'
        title = 'Edit game'
        game = get_object_or_404(Game, pk=game_id)
        if game.created_by != request.user.profile:
            return HttpResponseForbidden()
    else:
        url = 'add_game'
        title = 'Add game'
        game = Game(created_by=request.user.profile)

    form = GameForm(request.POST or None, instance=game)
    if request.POST and form.is_valid():
        game = form.save()

        # Create and attach new tags to game.
        tags = create_tags(game.description)
        if tags != []:
            game.tags.set(tags)
            game.save()

        return redirect('uploads')

    return render(
        request,
        'upsert_game.html',
        {
            **get_upsert_game_context(game, form, title, url)
        }
    )


# GET: Display games view
def games(request, *args, **kwargs):
    if request.method == 'GET':
        latest_games = Game.objects.order_by('-created_at')[:5]
        context = {
            **games_context,
            'latest': latest_games,
            'purchases': request.user.profile.purchases if request.user.is_authenticated else []
        }
        return render(request, 'games/games.html', context)
    return HttpResponse(status=404)


# GET: Display single game view
# POST: Add game
def game_details(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'GET':
        developer_context = None
        purchased = bool(Purchase.objects.filter(
            game=game_id,
            created_by=request.user.id,
            purchased_at__isnull=False
        ))
        if request.user.is_authenticated:
            if game.created_by.user.id == request.user.id:
                now = datetime.now(pytz.utc)
                developer_context = {
                    'reviews': {
                        'year': len(game.reviews.filter(
                            created_at__year=now.year
                        )),
                        'month': len(game.reviews.filter(
                            created_at__year=now.year,
                            created_at__month=now.month
                        )),
                        'pd': round(len(game.reviews.all()) / (
                            (now - game.created_at).total_seconds() / (60 * 60 * 24)
                        ), 2)
                    },
                    'purchases': {
                        'year': len(game.purchases.filter(
                            purchased_at__year=now.year
                        )),
                        'month': len(game.purchases.filter(
                            purchased_at__year=now.year,
                            purchased_at__month=now.month
                        )),
                        'pd': round(len(game.purchases.all()) / (
                            (now - game.created_at).total_seconds() / (60 * 60 * 24)
                        ), 2)
                    }
                }
        return render(
            request,
            'game_details.html',
            {
                'game': game,
                'purchased': purchased,
                'games': 'is-active',
                'crumbs': [
                    {
                        'label': 'Browse',
                        'url': 'games'
                    },
                    {'label': game.name},
                ],
                **developer_context,
            })
    return HttpResponse(status=404)  # other methods not supported


@login_required
def purchase_game(request, game_id):
    if request.method != 'GET':  # Only supports get -method
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

    # Create purchase that is not yet activated. It will be activated when the payment has been processed successfully
    purchase = Purchase(
        game=game,
        created_by=request.user.profile,
    )
    purchase.save()

    return render(request, 'purchase.html', {
        **get_purchase_context(purchase),
        'success_url': '{}?purchase_id={}'.format(request.build_absolute_uri('?'), purchase.id),
        'error_url': '{}?purchase_id={}'.format(request.build_absolute_uri('?'), purchase.id),
        'cancel_url': '{}?purchase_id={}'.format(request.build_absolute_uri('?'), purchase.id),
    })


# GET: Display games purchased
@login_required
def library(request, *args, **kwargs):
    if request.method == "GET":
        profile = request.user.profile
        return render(
            request,
            'games/library.html',
            {
                **library_context,
                'allow_play': [purchase.game for purchase in profile.purchases.all()],
                'purchases': profile.purchases.filter(purchased_at__isnull=False),
                'profile': "profile"
            }
        )
    return HttpResponse(status=404)


# GET: Display games uploaded
@login_required
@user_passes_test(is_developer)
def uploads(request, *args, **kwargs):
    if request.method == "GET":
        profile = request.user.profile
        purchases = []  # initialize empty array for listing purchases
        for game in profile.uploads.all():  # fetch purchases for each game
            purchases += game.purchases.all()
        return render(
            request,
            'games/uploads.html',
            {
                **uploads_context,
                'my_uploads': profile.uploads,
                'purchases': purchases
            }
        )
    return HttpResponse(status=404)


# GET: Display games uploaded
@login_required
def play(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    profile = request.user.profile
    # Only allow player to play game if he has bought it
    if profile.purchases and profile.purchases.filter(game=game).count() > 0:
        context = {'profile': profile, **get_play_game_context(game)}
        return render(request, 'play_game.html', context)
    # otherwise redirect to its details page
    return redirect('/games/{}'.format(game.id))


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
    return HttpResponse(status=404)  # other methods not supported


@login_required
def game_state(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'GET':
        save = get_object_or_404(Save, game=game, user=request.user.profile)
        return JsonResponse(save.game_state)
    elif request.method == 'POST':
        Save.objects.update_or_create(
            game=game,
            user=request.user.profile,
            defaults={'content': base64.encodebytes(request.body)},
        )
        return HttpResponse(status=201)
    return HttpResponse(status=404)  # other methods not supported
