from django.urls import path

from .views import (
    manage_review,
)

urlpatterns = [
    path('', manage_review, name='review'),
]
