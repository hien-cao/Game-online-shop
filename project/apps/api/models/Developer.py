from django.db import models

from .Game import Game
from .User import User

class Developer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

