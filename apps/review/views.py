from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
    JsonResponse
)

from ..game.models import Game
from .models import Review
from .forms import ReviewForm

@login_required
def delete_review(request, game_id):
    """ Enpoint update the game's review data as review is deleted """
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'DELETE':
        try: # We return the message to inform the success of review deletion 
            review = Review.objects.get(
                game=game,
                created_by=request.user.profile
            )
            review.delete()
            return JsonResponse({"message": "success"}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({"message": "Review not found!"}, status=404)
    return JsonResponse({"message": "Invalid request method!"}, status=400)

@login_required
def manage_review(request, game_id):
    """ Endpoint to handle the saving of a review """
    game = get_object_or_404(Game, pk=game_id)
    review, _ = Review.objects.get_or_create(
        game=game,
        created_by=request.user.profile
    )
    form = ReviewForm(request.POST or None, instance=review)
    # Handle loading the review page and redirect if the review is saved successfully 
    if request.method == 'POST' and request.POST and form.is_valid():
        review = form.save()
        messages.success(
            request,
            'Review successfully saved!'
        )
        return redirect('game_details', game_id=game_id)
    return render(
        request,
        'upsert_review.html', {
            'form': form,
            'game_id': game_id
        }
    )
