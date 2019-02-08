import pytz
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .models import ApiKey
from .utils.decorators import dev_api_request
from .utils.utils import get_profile

from ...game.models import Game
from ...review.models import Review


def _generate(profile):
    """Create an apikey for owner (`profile`)."""
    apikey = ApiKey.objects.create(owner=profile)
    apikey.save()
    return JsonResponse({"message": apikey.key})


def generate(request):
    """View for generating and replacing a developer's apikey."""
    if request.method == 'POST':
        if not request.user.profile.is_developer:
            return HttpResponse(status=401)
        try:
            existing_key = ApiKey.objects.get(owner=request.user.profile)
            existing_key.delete()
            return _generate(request.user.profile)
        except ObjectDoesNotExist:
            return _generate(request.user.profile)

    return HttpResponse(status=404)


@dev_api_request
def games(request, *args, **kwargs):
    """Endpoint for fetching data about games."""
    if kwargs['error_response']:
        return kwargs['error_response']
    game_set = Game.objects.filter(created_by=get_profile(request))
    return {
        "content": list(
            game_set.values('id', 'name', 'price')
        ),
        "count": len(game_set),
        "message": "Success!"
    }


@dev_api_request
def game(request, *args, **kwargs):
    """Endpoint for fetching data of one game."""
    if kwargs['error_response']:
        return kwargs['error_response']
    try:
        game = Game.objects.get(
            created_by=get_profile(request), pk=kwargs['game_id'])
        content = {
            **model_to_dict(game),
            "tags": [tag.name for tag in game.tags.all()]
        }
        return {
            "content": content,
            "count": 1,
            "message": "Success!"
        }
    except ObjectDoesNotExist:
        return {
            "message": "Invalid request. Game not found!"
        }

@dev_api_request
def my_reviews(request, *args, **kwargs):
    """Endpoint for fetching all reviews by requester."""
    if kwargs['error_response']:
        return kwargs['error_response']
    review_set = Review.objects.filter(created_by=get_profile(request))
    return {
        "content": list(review_set.values()),
        "count": len(review_set),
        "message": "Success!"
    }


@dev_api_request
def game_reviews(request, *args, **kwargs):
    """Endpoint for fetching all reviews for all requester's games."""
    if kwargs['error_response']:
        return kwargs['error_response']
    game_set = Game.objects.filter(created_by=get_profile(request))
    review_set = {}
    review_count = 0
    for game in game_set:
        review_set_for_game = Review.objects.filter(game=game)
        review_set[game.id] = list(review_set_for_game.values())
        review_count += len(review_set_for_game.values())
    return {
        "content": review_set,
        "count": review_count,
        "message": "Success!"
    }

@dev_api_request
def game_review(request, *args, **kwargs):
    """Endpoint for fetching all reviews for one game."""
    if kwargs['error_response']:
        return kwargs['error_response']
    try:
        game = Game.objects.get(created_by=get_profile(request), pk=kwargs['game_id'])
        review_set = {}
        review_set_for_game = Review.objects.filter(game=game)
        review_set[game.id] = list(review_set_for_game.values())
        return {
            "content": review_set,
            "count": 1,
            "message": "Success!"
        }
    except ObjectDoesNotExist:
        return {
            "message": "Invalid request. Game not found!"
        }

@dev_api_request
def game_statistics(request, *args, **kwargs):
    """Endpoint for fetching statistics of a game."""
    if kwargs['error_response']:
        return kwargs['error_response']
    try:
        game = Game.objects.get(created_by=get_profile(request), pk=kwargs['game_id'])
        # Query for the purchases and reviews list of the game
        purchases = game.purchases.filter(purchased_at__isnull=False)
        reviews = game.reviews
        # Create variable to contain current time
        now = datetime.now(pytz.utc)
        content = {}
        statistics = {
            'cummulative_revenue': sum([purchase.price for purchase in purchases]),
            'purchases': {
                'total_purchases': purchases.count(),
                'current_year_purchases': len(purchases.filter(purchased_at__year=now.year)),
                'current_month_purchases': len(purchases.filter(purchased_at__year=now.year, purchased_at__month=now.month)),
                'purchase_per_day': round(len(purchases.all())/((now - game.created_at).total_seconds()/(60 * 60 * 24)), 2)
            },
            'reviews': {
                'total_reviews': reviews.count(),
                'current_year_reviews': len(reviews.filter(created_at__year=now.year)),
                'current_month-reviews': len(reviews.filter(created_at__year=now.year, created_at__month=now.month)),
                'review_per_day': round(len(reviews.all()) / ((now - game.created_at).total_seconds() / (60 * 60 * 24)), 2)
            }
        }
        content[game.id] = statistics
        return {
            "content": content,
            "count": 1,
            "message": "Success!"
        }
    except ObjectDoesNotExist:
        return {
            "message": "Invalid request. Game not found!"
        }
