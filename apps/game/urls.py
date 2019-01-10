from django.urls import path

from .views import game, games, add_game, library, my

urlpatterns = [
    path('', games, name='games'),
    path('<int:game_id>', game, name='game'),
    path('add/', add_game, name='add_game'),
    path('library/', library, name='library'),
    path('my/', my, name='my')
]
