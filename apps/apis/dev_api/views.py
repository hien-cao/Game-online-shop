import pytz
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .models import ApiKey
from .utils.decorators import dev_api_request, validate_request, json_response
from .utils.utils import get_profile

from ...game.models import Game, Purchase
from ...review.models import Review

def _generate(profile):
    instance = ApiKey.objects.create(owner=profile)
    instance.save()
    return JsonResponse({"message": instance.key})


def generate(request):
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
    if kwargs['error_response']:
        return kwargs['error_response']
    query_set = Game.objects.filter(created_by=get_profile(request))
    return {
        "content": list(
            query_set.values('id', 'name', 'price')
        ),
        "count": len(query_set),
        "message": "Success!"
    }


@dev_api_request
def game(request, *args, **kwargs):
    if kwargs['error_response']:
        return kwargs['error_response']
    try:
        query_set = Game.objects.filter(
            created_by=get_profile(request), pk=kwargs['game_id'])
        if len(query_set) == 0:
            raise ObjectDoesNotExist('')
        content = [{
            **model_to_dict(obj),
            "tags": [tag.name for tag in query_set[0].tags.all()]
        } for obj in query_set]
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
    if kwargs['error_response']:
        return kwargs['error_response']
    query_set = Review.objects.filter(created_by=get_profile(request))
    return {
        "content": list(query_set.values()),
        "count": len(query_set),
        "message": "Success!"
    }


@dev_api_request
def game_reviews(request, *args, **kwargs):
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
    if kwargs['error_response']:
        return kwargs['error_response']
    try:
        game = Game.objects.filter(created_by=get_profile(request), pk=kwargs['game_id'])
        if len(game) == 0:
            raise ObjectDoesNotExist('')
        review_set = {}
        review_set_for_game = Review.objects.filter(game=game[0])
        review_set[game[0].id] = list(review_set_for_game.values())
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
    if kwargs['error_response']:
        return kwargs['error_response']
    try: 
        game = Game.objects.filter(created_by=get_profile(request), pk=kwargs['game_id'])
        if len(game) == 0:
            raise ObjectDoesNotExist('')
        # Query for the purchases and reviews list of the game
        purchases = game[0].purchases.filter(purchased_at__isnull=False)
        review = game[0].reviews
        # Create variable to contain current time
        now = datetime.now(pytz.utc)
        content = {}
        statistics = {
            'cummulative_revenue': sum([purchase.price for purchase in purchases]),
            'purchases': {
                'total_purchases': purchase.count(),
                'current_year_purchases': len(purchase.filter(purchased_at__year=now.year)),
                'current_month_purchases': len(purchase.filter(purchased_at__year=now.year, purchased_at__month=now.month)),
                'purchase_per_day': round(len(purchase.all())/((now - game[0].created_at).total_seconds()/(60 * 60 * 24)), 2)
            },
            'reviews': {
                'total_reviews': review.count(),
                'current_year_reviews': len(review.filter(created_at__year=now.year)),
                'current_month-reviews': len(review.filter(created_at__year=now.year, created_at__month=now.month)),
                'review_per_day': round(len(review.all()) / ((now - game[0].created_at).total_seconds() / (60 * 60 * 24)), 2)
            }
        }
        content[game[0].id] = statistics
        return {
            "content": content,
            "count": 1,
            "message": "Success!"
        }
    except ObjectDoesNotExist:
        return {
            "message": "Invalid request. Game not found!"
        }
    