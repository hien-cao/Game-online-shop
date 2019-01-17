from django.forms import ModelForm

from ..models import Game


# Create the form class.
class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'url', 'price']
