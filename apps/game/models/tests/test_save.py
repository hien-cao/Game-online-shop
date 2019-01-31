import base64
from django.test import TestCase

from ...models import Game, Purchase, Save
from ....user.utils.mock_user import create_mock_user


class SaveTestCase(TestCase):
    def setUp(self):
        # create users
        self.game_creator = create_mock_user(0)
        self.game_purchaser = create_mock_user(1)
        # create game
        self.game = Game.objects.create(
            name='game_0',
            created_by=self.game_creator.profile,
            price=1,
        )
        # create purchase
        self.purchase = Purchase.objects.create(
            price=self.game.price,
            game=self.game,
            created_by=self.game_purchaser.profile,
        )
        # create save
        self.save = Save.objects.create(
            game=self.game,
            user=self.game_purchaser.profile,
            content=base64.encodebytes(b'{"foo": "bar"}'),
        )

    def test_save_can_be_created(self):
        self.assertIsInstance(self.save, Save)

    def test_property_game_state(self):
        self.assertDictEqual(self.save.game_state, {"foo": "bar"})

    def test_save_is_not_created_if_no_purchase(self):
        self.purchase.delete()
        other_save = Save.objects.create(
            game=self.game,
            user=self.game_purchaser.profile,
            content=base64.encodebytes(b'{"foo": "bar"}')
        )
        self.assertIsInstance(other_save, Save)
        with self.assertRaises(Save.DoesNotExist):
            other_save.refresh_from_db()
