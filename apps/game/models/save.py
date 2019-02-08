from django.db import models
import base64
import json

from ...user.models import Profile
from ...game.models import Game, Purchase


class Save(models.Model):
    """
    Save model.
    - game: Game
    - user: Profile
    - content: BinaryField
    """
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    # We store game state as base64 encoded string
    content = models.BinaryField()

    class Meta:
        # Should only allow single save for each user per game (multiple saves were not specified)
        # Creating a new save should overwrite previously created
        unique_together = ('game', 'user')

    @property
    def game_state(self):
        """Get state of the game from binary as json."""
        return json.loads(base64.decodebytes(self.content).decode('utf-8'))

    def save(self, *args, **kwargs):
        """Only saves to games purchased are allowed"""
        if Purchase.objects.filter(
            game=self.game,
            created_by=self.user,
            purchased_at__isnull=False
        ):
            super(Save, self).save(*args, **kwargs)
