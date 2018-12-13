from django.db import models

from . import LoadState

class PlayDetails(models.Model):
    purchased = models.BooleanField(default=False)
    times_played = models.IntegerField()
    score = models.BigIntegerField()
    player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE
    )
    # load_state = models.OneToOneField(
    #     LoadState,
    #     on_delete=models.CASCADE
    # )
