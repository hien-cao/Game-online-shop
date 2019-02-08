import os
import uuid
from django.utils import timezone
from hashlib import md5
from django.db import models

from ...user.models import Profile
from ...game.models import Game

assert os.environ['PAYMENT_API_URI'] is not None
assert os.environ['PAYMENT_API_SELLER_ID'] is not None
assert os.environ['PAYMENT_API_KEY'] is not None


class Purchase(models.Model):
    """
    Purchase model.
    - id: UUIDField
    - [purchased_at] = DateTimeField
    - price = DecimalField
    - [ref] = IntegerField
    - game: Game
    - created_by: Profile
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchased_at = models.DateTimeField(
        auto_now_add=False, null=True, blank=True, editable=True)
    # set separate price field for purchases
    # (as it may depending if there is an active discount)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # we probably want to store ref number
    # (in case if we could query against payment api)
    ref = models.IntegerField(null=True)
    game = models.ForeignKey(
        Game,
        related_name='purchases',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        Profile,
        related_name='purchases',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('game', 'created_by')

    # helper property for payment id, since the payment api does not accept special characters (including '-')
    @property
    def pid(self):
        return str(self.id).replace('-', '')

    def save(self, *args, **kwargs):
        # Delete previously failed (and not accepted) purchases for given user and game
        Purchase.objects.filter(
            game=self.game,
            created_by=self.created_by,
            purchased_at__isnull=True
        ).exclude(pk=self.pk).delete()

        if self.price is None:
            self.price = self.game.price
        super(Purchase, self).save()

    def get_payment_context(self):
        """Get relevant information regarding a payment."""
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
        """Activates a purchase if query matches the checksum."""
        purchase = Purchase.objects.get(pk=query.get('purchase_id'))
        # having data in purchased_at field implies that
        # the game has been purchased
        assert purchase.purchased_at is None
        # calculate expected response checksum and
        # compare it the one provided by api
        if md5(
            'pid={}&ref={}&result={}&token={}'
            .format(
                purchase.pid,
                query.get('ref'),
                query.get('result'),
                os.environ['PAYMENT_API_KEY']
            )
            .encode("ascii")
        ).hexdigest() == query.get('checksum'):
            purchase.purchased_at = timezone.now()
            # update the payment reference received
            purchase.ref = query.get('ref')
            purchase.save()
        # else just does nothing and returns to payment page.
        # As this wont happen without meddling with the request params,
        # we wont return error message

    @staticmethod
    def cancel(purchase_id):
        """Cancel a purchase."""
        purchase = Purchase.objects.get(pk=purchase_id)
        # only non-paid purchases can be cancelled
        assert purchase.purchased_at is None
        purchase.delete()  # no need to track cancelled payments
