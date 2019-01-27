from django.urls import include, path

from .views import generate, games, game, my_reviews, game_reviews

urlpatterns = [
    path('generate/', generate, name='dev-api-generate'),
    path('games/', games, name='dev-api-games'),
    path('games/<int:game_id>', game, name='dev-api-game'),
    path('my-reviews/', my_reviews, name='dev-api-my-reviews'),
    path('game-reviews/', game_reviews, name='dev-api-game-reviews'),
]
