from django.db import models

class GameCategory(models.Model):
    game_id = models.OneToOneField(
        'Game',
        on_delete=models.CASCADE,
    )
    category_id = models.OneToOneField(
        'Category',
        on_delete=models.CASCADE,
    )