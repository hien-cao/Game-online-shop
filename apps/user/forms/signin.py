from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignInForm(AuthenticationForm):
    """
    Form for sign in.

    Only allows login for users that have confirmed their email.
    """
    def confirm_login_allowed(self, user):
        if not user.profile.email_confirmed:
            raise forms.ValidationError(
                'Email for this user has not yet been confirmed.',
                code='not_confirmed'
            )
