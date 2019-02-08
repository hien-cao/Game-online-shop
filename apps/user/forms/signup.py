from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=256,
        help_text='Required. Please provide a valid email address.'
    )
    is_developer = forms.BooleanField(
        required=False,
        label='I\'m a developer',
        help_text='Optional. This field may be changed later.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'is_developer', 'password1', 'password2')
