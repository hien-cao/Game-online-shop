from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .purchase import Purchase
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

    def save(self, *args, **kwargs):
        """
        @Override the save so that it:
        -   Only allows storing a highscore for those players
            that have purchased the game.
        """
        try:
            Purchase.objects.get(game=self.game, created_by=self.created_by)
            super(Highscore, self).save(*args, **kwargs)
            return {"message": "score saved!"}
        except ObjectDoesNotExist:
            return {"message": "invalid request!"}
