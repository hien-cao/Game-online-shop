from django.urls import path

from .views import games, add_game, library, my, play, save_score

urlpatterns = [
    path('', games, name='games'),
    path('add/', add_game, name='add_game'),
    path('library/', library, name='library'),
    path('my/', my, name='my'),
    path('<int:game_id>/play', play, name='play'),
    path('<int:game_id>/save-score', save_score, name='save_score')
]