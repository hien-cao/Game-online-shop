from django.urls import path, re_path

from .views.game import GameView
from .views.developer import DeveloperView

urlpatterns = [
    path('game/', GameView.as_view()),
    path('dev/', DeveloperView.as_view()),
]