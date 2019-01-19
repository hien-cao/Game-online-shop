from django.forms import ModelForm, Textarea

from ..models import Game


# Create the form class.
class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'url', 'price', 'description']
        help_texts = {
            'description': 'Note: You can add tags to your game such as "#adventure"',
        }
        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }
