from django.urls import include, path

from .views import generate

urlpatterns = [
    path('generate', generate, name='generate')
]
