from django.db import models

from ...user.models import Profile

class Purchase(models.Model):
    purchased_at = models.DateField()
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
