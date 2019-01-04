from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    is_developer = models.BooleanField(default=False)
    games = models.ManyToManyField(
        'game.Game',
        through='game.Purchase',
        blank=True
    )

    def __str__(self):
        return self.user.username
