from django.utils import timezone
from django.test import TestCase

from ...models import Game, Highscore, Purchase
from ....user.utils.mock_user import create_mock_user


class HighscoreTestCase(TestCase):
    def setUp(self):
        # create a game
        self.game = Game.objects.create(
            name="game",
            url="https://localhost:3000",
            price=0,
        )
        # create a user
        self.user = create_mock_user(2)
        # create a purchase
        self.purchase = Purchase.objects.create(
            game=self.game,
            created_by=self.user.profile,
            purchased_at=timezone.now()
        )

    def test_highscore_can_be_created(self):
        """Create a highscore and assert."""
        highscore = Highscore.objects.create(
            score=10,
            game=self.game,
            created_by=self.user.profile
        )
        self.assertIsInstance(highscore, Highscore)

    def test_highscore_cannot_be_updated(self):
        """Create a highscore, try save again and assert."""
        highscore = Highscore.objects.create(
            score=10,
            game=self.game,
            created_by=self.user.profile
        )
        self.assertEqual(highscore.save()["message"], "update is prohibited!")
