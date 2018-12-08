from django.db import models

from .Developer import Developer
from .GameCategory import GameCategory
from .PlayDetails import PlayDetails

class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField(unique=True)
    price = models.FloatField()
    developer = models.ForeignKey(
        Developer,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def categories(self):
        return GameCategory.objects.filter(game_id=self.pk)
