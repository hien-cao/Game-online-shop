from django.forms import ModelForm, Textarea, HiddenInput
from ..models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['grade', 'content']
        help_texts = {
            'content': """
                Note: This service is for people of all ages.
                Please do not use provocative language!"""
        }
        widgets = {
            'grade': HiddenInput(),
            'content': Textarea(attrs={'rows': 4}),
        }
