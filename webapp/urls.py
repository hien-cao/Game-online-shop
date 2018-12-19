from django.urls import path, re_path

from .views.loggedout import home, register

urlpatterns = [
    # Register view
    path('', home, name='home'),
    path('register/', register, name='register')
]