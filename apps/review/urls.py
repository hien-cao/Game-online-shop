from django.urls import path

from .views import (
    manage_review,
    delete_review,
)

urlpatterns = [
    path('', manage_review, name='review'),
    path('delete/', delete_review, name='delete-review'),
]
