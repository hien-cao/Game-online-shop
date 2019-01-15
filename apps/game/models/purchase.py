import requests
import os
import uuid
from django.db import models

from ...user.models import Profile
from ...game.models import Game

assert os.environ['PAYMENT_API_URI'] is not None
assert os.environ['PAYMENT_API_SELLER_ID'] is not None
assert os.environ['PAYMENT_API_KEY'] is not None

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchased_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    # set separate price field for purchases (as it may depending if there is an active discount)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    def save(self):
        self.price = self.game.price
        if True:
            # requests.post(
            #     os.environ['PAYMENT_API_URI'],
            #     data={
            #         'pid': '',
            #         'sid': os.environ['PAYMENT_API_SELLER_ID'],
            #         'amount': self.price,
            #         'success_url': '',
            #         'cancel_url': '',
            #         'error_url': '',
            #         'checksum': '',
            #     }
            # )
            super(Purchase, self).save()
        else:
            return
