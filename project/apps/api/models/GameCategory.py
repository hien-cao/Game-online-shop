from django.db import models

from .Category import Category
from .Game import Game

class GameCategory(models.Model):
    game_id = models.OneToOneField(
        Game,
        on_delete=models.CASCADE,
    )
    category_id = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
    )
