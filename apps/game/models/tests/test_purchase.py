from django.utils import timezone
from django.test import TestCase
from django.forms.models import model_to_dict

from ...models import Game, Purchase
from ....user.utils.mock_user import create_mock_user

DUMMY_PID = 'abc123'
DUMMY_REF = 1
DUMMY_RESULT = 'success'


class PurchaseTestCase(TestCase):
    def setUp(self):
        # create users
        self.game_creator = create_mock_user(0)
        self.game_purchaser = create_mock_user(1)
        # create a game to purchase
        self.game = Game.objects.create(
            name='game_0',
            created_by=self.game_creator.profile,
            price=1,
        )
        self.purchase = Purchase.objects.create(
            price=self.game.price,
            game=self.game,
            created_by=self.game_purchaser.profile,
        )

    def tearDown(self):
        if self.purchase.purchased_at:
            self.purchase.purchased_at = None
            self.purchase.save()

    def test_purchase_can_be_created(self):
        """Create a purchase and assert."""
        purchase = Purchase.objects.create(
            price=self.game.price,
            game=self.game,
            created_by=self.game_purchaser.profile,
        )
        self.assertIsInstance(purchase, Purchase)

    def test_purchase_can_be_updated(self):
        """Try to update, refresh and assert."""
        purchase_timestamp = timezone.now()
        self.purchase.purchased_at = purchase_timestamp
        self.purchase.ref = DUMMY_REF
        self.purchase.save()
        self.purchase.refresh_from_db()
        self.assertIsInstance(self.purchase, Purchase)
        self.assertEqual(self.purchase.ref, DUMMY_REF)
        self.assertEqual(self.purchase.purchased_at, purchase_timestamp)

    def test_property_pid(self):
        """See that pid property exists and does not contain '-'"""
        self.assertIsNotNone(self.purchase.pid)
        self.assertNotIn(self.purchase.pid, '-')

    def test_payment_context(self):
        """See that payment context is contains all key, value pairs"""
        context = self.purchase.get_payment_context()
        self.assertIsNotNone(context)
        for _, value in context.items():
            self.assertIsNotNone(value)

    def test_activate(self):
        """activate() should be only allowed to be done once."""
        query = {
            'purchase_id': self.purchase.id,
            'ref': DUMMY_REF,
            'result': DUMMY_RESULT,
            'checksum': self.purchase.get_payment_context()['checksum']
        }
        self.purchase.activate(query)
        purchase_as_dict = model_to_dict(self.purchase)
        self.assertIn('purchased_at', purchase_as_dict)
        self.assertIn('ref', purchase_as_dict)
        self.assertRaises(AssertionError, self.purchase.activate(query))

    def test_cancel(self):
        pass
