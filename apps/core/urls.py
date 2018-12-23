from django.urls import path, re_path

# from .views.game import add_game, delete_game, GameView
# from .views.developer import DeveloperView

from .views import home, terms_and_conditions

urlpatterns = [
    path('', home, name='home'),
    path('terms-and-conditions/', terms_and_conditions, name='terms-and-conditions'),
]