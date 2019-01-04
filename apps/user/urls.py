from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from .views import welcome

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path('^oauth/', include('social_django.urls')),
    path('welcome/', welcome, name='welcome')
]