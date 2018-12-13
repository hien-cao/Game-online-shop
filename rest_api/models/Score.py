from django.db import models

class Score(models.Model):
    player = models.OneToOneField(
        'Player',
        on_delete=models.CASCADE
    )
    points = models.IntegerField()
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='scores'
    )

    def __str__(self):
        return self.points

