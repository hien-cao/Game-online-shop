from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from .views import welcome, account_activation_sent, activate, register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
        template_name='login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path('^oauth/', include('social_django.urls')),
    re_path('^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('welcome/', welcome, name='welcome')
]