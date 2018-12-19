from django.db import models

class GameCategory(models.Model):
    game = models.OneToOneField(
        'Game',
        on_delete=models.CASCADE,
    )
    category = models.OneToOneField(
        'Category',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}: {}".format(self.game, self.category)