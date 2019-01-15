from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from .forms import SignInForm
from .views import (
    welcome,
    account_activation_sent,
    activate,
    signup,
    signout
)
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', auth_views.LoginView.as_view(
        authentication_form=SignInForm,
        redirect_authenticated_user=True,
        template_name='signin.html'
    ), name='signin'),
    path('signout/', signout, name='signout'),
    re_path('^oauth/', include('social_django.urls')),
    re_path('^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('welcome/', welcome, name='welcome')
]