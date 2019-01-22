from django.urls import path

from .views import (
    game_details,
    games,
    manage_game,
    library,
    uploads,
    play,
    save_score,
    purchase_game,
    search,
    autosuggestion_search
)

urlpatterns = [
    path('', games, name='games'),
    path('search/', search, name='search'),
    path('search/search-term/<query>',
         autosuggestion_search, name='autosuggestion'),
    path('<int:game_id>/', game_details, name='game_details'),
    path('<int:game_id>/purchase/', purchase_game, name='purchase_game'),
    path('add/', manage_game, name='add_game'),
    path('uploads/', uploads, name='uploads'),
    path('<int:game_id>/play/', play, name='play'),
    path('<int:game_id>/save-score/', save_score, name='save_score'),
    path('library/', library, name='library'),
    path('<int:game_id>/edit/', manage_game, name='edit_game'),
]
