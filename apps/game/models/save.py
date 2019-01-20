from django.db import models
import base64
import json

from ...user.models import Profile
from ...game.models import Game

class Save(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    content = models.BinaryField() # We store game state as base64 encoded string

    class Meta:
        # Should only allow single save for each user per game (multiple saves were not specified)
        # Creating a new save should overwrite previously created
        unique_together = ('game', 'user')

    @property
    def game_state(self):
        return json.loads(base64.decodebytes(self.content).decode('utf-8'))
