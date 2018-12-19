from django.urls import path, re_path

from .views.game import add_game, delete_game, GameView
from .views.developer import DeveloperView

urlpatterns = [
    # Game model URLs
    path('game/add/', add_game, name='add-game'),
    path('game/<int:id>/', GameView.as_view()),
    path('game/<int:id>/delete/', delete_game, name='delete-game'),

    # Developer model URLs
    path('dev/', DeveloperView.as_view()),
]