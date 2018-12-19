from django.db import models

from . import GameCategory, PlayDetails

class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)
    url = models.URLField(unique=True)
    price = models.FloatField()
    # createdAt
    developer = models.ForeignKey(
        'Developer',
        on_delete=models.CASCADE,
        related_name='games',
        null=True
    )

    def __str__(self):
        return self.name

    def categories(self):
        return GameCategory.objects.filter(game_id=self.pk)
