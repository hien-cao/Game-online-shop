from django.urls import path

from .views import (
    game_details,
    games,
    add_game,
    library,
    uploads,
    play,
    save_score,
    purchase_game,
)

urlpatterns = [
    path('', games, name='games'),
    path('<int:game_id>/', game_details, name='game_details'),
    path('<int:game_id>/purchase', purchase_game, name='purchase_game'),
    path('add/', add_game, name='add_game'),
    path('uploads/', uploads, name='uploads'),
    path('<int:game_id>/play/', play, name='play'),
    path('<int:game_id>/save-score/', save_score, name='save_score'),
    path('library/', library, name='library'),
]
