from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    games = models.ManyToManyField(
        'Game',
        through='PlayDetails'
    )
    is_player = models.BooleanField(default=True)
