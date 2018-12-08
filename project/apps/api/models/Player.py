from django.db import models

from .Game import Game
from .User import User

class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    games = models.ManyToManyField(
        Game,
        through='PlayDetails'
    )
