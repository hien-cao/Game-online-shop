from django.urls import path

from .views import games, add_game, library, my

urlpatterns = [
    path('', games, name='games'),
    path('add/', add_game, name='add_game'),
    path('library/', library, name='library'),
    path('my/', my, name='my'),
    # path('<int:id>/', game, name='game')
]