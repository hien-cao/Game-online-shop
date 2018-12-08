from django.db import models

from .Player import Player

class Score(models.Model):
    player = models.OneToOneField(
        Player,
        on_delete=models.CASCADE
    )
    points = models.IntegerField()
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='scores'
    )

