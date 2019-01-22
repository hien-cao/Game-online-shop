from django.shortcuts import render, redirect, get_object_or_404
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
def manage_review(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    review, _ = Review.objects.get_or_create(
        game=game,
        created_by=request.user.profile
    )
    form = ReviewForm(request.POST or None, instance=review)
    if request.POST and form.is_valid():
        review = form.save()

        return redirect('game_details', game_id=game_id)

    return render(
        request,
        'upsert_review.html', {
            'form': form,
            'game_id': game_id
        }
    )
