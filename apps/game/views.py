import json
import base64
import re
import pytz
from datetime import datetime

from django.contrib.auth.models import User
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
    uploads_context,
    get_play_game_context,
    get_upsert_game_context,
    get_purchase_context,
    get_paginated_context,
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


def find_template_name(order_by):
    if order_by == 'created_at':
        return 'latest'
    return None


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
        order_by = request.GET.get('order_by') or 'name'
        if request.GET.get('page') and hasattr(Game, order_by):
            try:  # Try to convert page param to int
                page = max(1, int(request.GET.get('page')))
            except ValueError:
                page = 1
            items = request.GET.get('items') or 20
            total_count = Game.objects.count()
            if order_by == 'created_at':
                games = Game.objects.order_by(
                    '{0}{1}'.format('-' if request.GET.get('desc') else '', order_by)
                )[(page - 1) * items:page * items]
            else:
                # NOTE: This method of querying is inefficient as
                # we have to query all results from database before filtering.
                # This is because it is not possible to filter by property.
                all_games = Game.objects.all()
                games = list(filter(lambda x: getattr(x, order_by), all_games))[(page - 1) * items:page * items]
            context = {
                **games_context,
                **get_paginated_context(order_by, page, items, total_count, games)
            }
        else:
            # Get all games because it is not possible to use
            # properties created with python (not db).
            all_games = Game.objects.all()
            latest_games = Game.objects.order_by('-created_at')[:5]
            popular_games = list(filter(lambda x: x.grade, all_games))[:5]
            context = {
                **games_context,
                'latest': latest_games,
                'popular': popular_games,
                'purchases': request.user.profile.purchases if request.user.is_authenticated else []
            }
        return render(request, 'games/games.html', context)
    return HttpResponse(status=404)


# GET: Display single game view
# POST: Add game
def game_details(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'GET':
        developer_context = {}
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
        purchases = Purchase.objects.none()  # initialize empty queryset for listing purchases
        for game in profile.uploads.all():  # fetch purchases for each game
            purchases |= game.purchases.all()
        purchases = purchases.order_by('-purchased_at')
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


# Autosuggestion for search query
def autosuggestion_search(request):
    if request.method == 'GET':
        results = []
        if request.GET.get('tag'):
            query = request.GET.get('tag')
            categories = Tag.objects.filter(name__icontains=query)
            for category in categories:
                results.append(category.name)
        elif request.GET.get('author'):
            query = request.GET.get('author')
            users = User.objects.filter(username__icontains=query)
            developers = Profile.objects.filter(user__in=users, is_developer=True)
            for developer in developers:
                results.append('@' + developer.user.username)
        else:
            query = request.GET.get('name')
            games = Game.objects.filter(name__icontains=query)
            for game in games:
                results.append(game.name)

        data = json.dumps({"results": results})
        return HttpResponse(data)
    return HttpResponse(staus=404)


# Autosuggestion for search query if the search from library page
@login_required
def autosuggestion_search_library(request):
    if request.method == 'GET':
        purchases = request.user.profile.purchases.filter(purchased_at__isnull=False)
        results = []
        if request.GET.get('tag'):
            query = request.GET.get('tag')
            categories = Tag.objects.filter(name__icontains=query)
            for category in categories:
                for purchase in purchases:
                    if category in purchase.game.tags:
                        results.append(category.name)
        elif request.GET.get('author'):
            query = request.GET.get('author')
            users = User.objects.filter(username__icontains=query)
            developers = Profile.objects.filter(user__in=users, is_developer=True)
            for developer in developers:
                for purchase in purchases:
                    if developer == purchase.game.created_by:
                        results.append('@' + developer.user.username)
        else:
            query = request.GET.get('name')
            games = Game.objects.filter(name__icontains=query)
            for game in games:
                for purchase in purchases:
                    if game == purchase.game:
                        results.append(game.name)

        data = json.dumps({"results": list(set(results))})
        return HttpResponse(data)
    return HttpResponse(staus=404)


# Search for the games by categories, developer, and game name
def search(request):
    if request.method == 'GET':
        # Path of the request
        path = request.path
        # Path of the search from browse
        browse = "/games/search/"
        # Path of the search from library
        library = "/games/library/search/"
        context = {}
        games = []
        #  Collect the data that match the search
        if 'search_term' in request.GET:
            query = request.GET['search_term']
            if not query:
                return HttpResponseRedirect('/games' if path == browse else '/games/library')

            if '#' == query[0]:
                tag = Tag.objects.filter(name=query)
                games = Game.objects.filter(tags__in=tag).order_by('created_at')[:5]
            elif "@" == query[0]:
                user_query = query.replace('@', '')
                user = User.objects.filter(username=user_query)
                developer = Profile.objects.filter(user__in=user, is_developer=True)
                games = Game.objects.filter(created_by__in=developer).order_by('created_at')[:5]
            else:
                games = Game.objects.filter(name__icontains=query).order_by('created_at')[:5]

            context['query'] = query
            context['latest'] = games
            # Preserve the search input
            context['value'] = request.GET

        if path == browse:
            # Add class is-active
            context['games'] = 'is-active'
            return render(request, 'games/games.html', context)
        elif path == library and request.user.is_authenticated:
            purchases = request.user.profile.purchases.filter(purchased_at__isnull=False, game__in=games)
            context['purchases'] = purchases
            # Preserve the search input
            context['library'] = 'is-active'
            return render(request, 'games/library.html', context)
    return HttpResponse(status=404)


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
