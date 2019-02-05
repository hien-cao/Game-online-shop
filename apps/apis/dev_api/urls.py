from django.urls import include, path

from .views import generate, games, game, my_reviews, game_reviews, game_review, game_statistics

urlpatterns = [
    path('generate/', generate, name='dev-api-generate'),
    path('games/', games, name='dev-api-games'),
    path('games/<int:game_id>/', game, name='dev-api-game'),
    path('game-statistics/<int:game_id>/', game_statistics, name='dev-api-game-statistics'),
    path('my-reviews/', my_reviews, name='dev-api-my-reviews'),
    path('game-reviews/', game_reviews, name='dev-api-game-reviews'),
    path('game-reviews/<int:game_id>/', game_review, name='dev-api-game-review'),
]
