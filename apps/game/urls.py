from django.urls import path, include

from .views import (
    game_details,
    games,
    game_state,
    manage_game,
    library,
    uploads,
    play,
    save_score,
    purchase_game,
    search,
    autosuggestion_search,
    autosuggestion_search_library
)

urlpatterns = [
    path('', games, name='games'),
    path('search/', search, name='search'),
    path('library/search/', search, name='search'),
    path('search/search-term/', autosuggestion_search, name='autosuggestion'),
    path('library/search/search-term/', autosuggestion_search_library, name='autosuggestion_library'),
    path('<int:game_id>/', game_details, name='game_details'),
    path('<int:game_id>/purchase/', purchase_game, name='purchase_game'),
    path('add/', manage_game, name='add_game'),
    path('uploads/', uploads, name='uploads'),
    path('<int:game_id>/play/', play, name='play'),
    path('<int:game_id>/save-score/', save_score, name='save_score'),
    path('<int:game_id>/state/', game_state, name='game_state'),
    path('library/', library, name='library'),
    path('<int:game_id>/edit/', manage_game, name='edit_game'),
    path('<int:game_id>/review/', include('apps.review.urls')),
]
