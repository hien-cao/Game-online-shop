from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class SignInForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.profile.email_confirmed:
            raise forms.ValidationError(
                'Email for this user has not yet been confirmed.',
                code='not_confirmed'
            )
