from django.urls import path

from .views import single_game, games, add_game, library, my

urlpatterns = [
    path('', games, name='games'),
    path('<int:game_id>', single_game, name='single_game'),
    path('add/', add_game, name='add_game'),
    path('library/', library, name='library'),
    path('my/', my, name='my')
]
