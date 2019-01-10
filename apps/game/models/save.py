from django.db import models

from ...user.models import Profile

class Save(models.Model):
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    content = models.TextField()
