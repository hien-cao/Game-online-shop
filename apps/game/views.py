import json
import base64
import re

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

from ..user.models import Profile
from .models import Game, Purchase, Highscore, Tag, Save
from .contexts import (
    games_context,
    library_context,
    my_context,
    get_play_game_context,
    get_upsert_game_context
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
        print(latest_games)
        context = {
            'latest': latest_games,
            **games_context,
        }
        return render(request, 'games/games.html', context)
    return HttpResponse(status=404)

# GET: Display single game view
# POST: Add game


def game_details(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'GET':
        purchased = bool(Purchase.objects.filter(
            game=game_id, created_by=request.user.id, purchased_at__isnull=False))
        if request.user.is_authenticated:
            if game.created_by.user.id == request.user.id:
                # TODO Render (and return) developer view
                pass
        return render(request, 'game_details.html', {'game': game, 'purchased': purchased})
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
    return redirect('games')


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

# Autosuggestion for search query


def autosuggestion_search(request, query=None):
    if request.method == 'GET':
        if query:
            results = []
            # term value from the games.html
            if '#' in query:
                query = query.replace('#', '')
                categories = Tag.objects.filter(name__icontains=query)
                for category in categories:
                    results.append(category.name)
            elif '@' in query:
                query = query.replace('@', '')
                developers = Profile.objects.filter(
                    name__icontains=query).filter(is_developer=True)
                for developer in developers:
                    results.append(developer.name)
            elif query:
                games = Game.objects.filter(name__icontains=query)
                for game in games:
                    results.append(game.name)
            else:
                results = []
        else:
            results = []
        data = json.dumps({"results": results})
        return HttpResponse(data)
    return HttpResponse(staus=404)

# Search for the games by categories, developer, and game name


def search(request):
    if request.method == 'GET':
        lastest_games = Game.objects.order_by('created_at')
        context = {}
        #  Collect the data that match the search
        if 'search_term' in request.GET:
            query = request.GET['search_term']
            if query:
                if '#' == query[0]:
                    query = query.replace('#', '')
                    latest_games = lastest_games.filter(tags=query)[:5]
                elif "@" == query[0]:
                    query = query.replace('@', '')
                    latest_games = lastest_games.filter(created_by=query)[:5]
                else:
                    latest_games = lastest_games.filter(name=query)[:5]

            if latest_games.count() != 0:
                context['latest'] = latest_games
            else:
                context['not_found'] = 'There is no result in the search'
        return render(request, 'games.html', context)
    return HttpResponse(status=404)


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
