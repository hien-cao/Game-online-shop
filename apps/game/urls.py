from django.urls import path

from .views import games, library, my

urlpatterns = [
    path('', games, name='games'),
    path('library/', library, name='library'),
    path('my/', my, name='my')
]