from django.db import models

from ...user.models import Profile

class Highscore(models.Model):
    score = models.IntegerField()
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
