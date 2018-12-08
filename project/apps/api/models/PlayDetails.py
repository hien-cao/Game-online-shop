from django.db import models

from .LoadState import LoadState

class PlayDetails(models.Model):
    purchased = models.BooleanField(default=False)
    times_played = models.IntegerField()
    score = models.BigIntegerField()
    load_state = models.OneToOneField(
        LoadState,
        on_delete=models.CASCADE
    )
