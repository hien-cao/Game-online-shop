import requests
from django.db import models

from ...user.models import Profile

class Purchase(models.Model):
    purchased_at = models.DateField()
    # set separate price field for purchases (as it may depending if there is an active discount)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    def save(self):
        if True:
            super().save()
        else:
            return
