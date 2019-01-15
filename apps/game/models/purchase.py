import os
import uuid
from datetime import datetime
from hashlib import md5
from django.db import models

from ...user.models import Profile
from ...game.models import Game

assert os.environ['PAYMENT_API_URI'] is not None
assert os.environ['PAYMENT_API_SELLER_ID'] is not None
assert os.environ['PAYMENT_API_KEY'] is not None

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchased_at = models.DateTimeField(auto_now_add=False, null=True, blank=True, editable=True)
    # set separate price field for purchases (as it may depending if there is an active discount)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ref = models.IntegerField(null=True) # we probably want to store ref number (in case if we could query against payment api)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    # helper property for payment id, since the payment api does not accept special characters (including '-')
    @property
    def pid(self):
        return str(self.id).replace('-', '')

    def save(self):
        if self.price is None:
            self.price = self.game.price
        super(Purchase, self).save()

    def get_payment_context(self):
        return {
            'pid': self.pid,
            'uri': os.environ['PAYMENT_API_URI'],
            'sid': os.environ['PAYMENT_API_SELLER_ID'],
            'amount': self.price,
            'checksum': md5(
                'pid={}&sid={}&amount={}&token={}'
                .format(
                    self.pid,
                    os.environ['PAYMENT_API_SELLER_ID'],
                    self.price,
                    os.environ['PAYMENT_API_KEY']
                )
                .encode("ascii")
            ).hexdigest()
        }

    @staticmethod
    def activate(query):
        purchase = Purchase.objects.get(pk=query.get('purchase_id'))
        assert purchase.purchased_at is None # having data in purchased_at field implies that the game has been purchased
        if md5( # calculate expected response checksum and compare it the one provided by api
            'pid={}&ref={}&result={}&token={}'
            .format(
                purchase.pid,
                query.get('ref'),
                query.get('result'),
                os.environ['PAYMENT_API_KEY']
            )
            .encode("ascii")
        ).hexdigest() == query.get('checksum'):
            purchase.purchased_at = datetime.now()
            purchase.ref = query.get('ref') # update the payment reference received
            purchase.save()
        # else just does nothing and returns to payment page.
        # As this is wont happen without meddling with the request params, we wont return error message

    @staticmethod
    def cancel(purchase_id):
        purchase = Purchase.objects.get(pk=purchase_id)
        assert purchase.purchased_at is None # only non-paid purchases can be cancelled
        purchase.delete() # no need to track cancelled payments
