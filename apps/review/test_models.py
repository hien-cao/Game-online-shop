from django.utils import timezone
from django.test import TestCase

from .models import Review
from ..game.models import Game, Purchase
from ..user.utils.mock_user import create_mock_user

DUMMY_REF = 1


class ReviewTestCase(TestCase):
    def setUp(self):
        # Create users
        self.game_creator = create_mock_user(0)
        self.purchaser_and_reviewer = create_mock_user(1)
        # Create a game
        self.game = Game.objects.create(
            name="game",
            created_by=self.game_creator.profile,
            price=0
        )
        # Create a purchase
        self.purchase = Purchase.objects.create(
            game=self.game,
            price=self.game.price,
            created_by=self.purchaser_and_reviewer.profile,
            purchased_at=timezone.now(),
            ref=DUMMY_REF
        )

    def test_review_can_be_created_if_purchased(self):
        """A review can be created if user has purchased game"""
        review = Review.objects.create(
            game=self.game,
            created_by=self.purchaser_and_reviewer.profile,
            created_at=timezone.now(),
            grade=5
        )
        self.assertIsInstance(review, Review)

    def test_review_cannot_be_created_if_no_purchase(self):
        """A review cannot be created if user has not purchased game"""
        not_purchased_user = create_mock_user(2)
        Review.objects.create(
            game=self.game,
            created_by=not_purchased_user.profile,
            created_at=timezone.now(),
            grade=0
        )
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(
                game=self.game,
                created_by=not_purchased_user.profile
            )
