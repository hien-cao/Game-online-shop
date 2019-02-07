from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from ..game import Game
from ..purchase import Purchase
from ....review.models import Review

from ....user.utils.mock_user import create_mock_user

TWOPLACES = Decimal(10) ** -2

orig_value = {
    'name': 'game_0',
    'description': 'foo',
    'url': 'https://localhost:7999/',
    'price': 0
}
new_value = {
    'name': 'game_1',
    'description': 'bar',
    'url': 'https://localhost:7998/',
    'price': 0.01
}


class GameTestCase(TestCase):
    def setUp(self):
        """Set up some variables used in some tests."""
        # Create object without reviews
        self.no_grade = Game.objects.create(
            name='no_grade',
            url='https://localhost:8000/',
            price=0,
        )
        # Create some mock users
        self.user_0 = create_mock_user()
        self.user_1 = create_mock_user(1)
        # Create object with reviews
        self.with_grade = Game.objects.create(
            name='with_grade',
            url='https://localhost:8001/',
            price=0,
        )
        Purchase.objects.create(
            created_by=self.user_1.profile,
            game=self.with_grade,
            purchased_at=timezone.now(),
            price=10,
        )
        Purchase.objects.create(
            created_by=self.user_0.profile,
            game=self.with_grade,
            purchased_at=timezone.now(),
            price=10,
        )
        # Create mock review
        Review.objects.create(
            game=self.with_grade,
            created_by=self.user_0.profile,
            grade=5,
        )

    def test_games_can_be_created(self):
        """Create a game and assert."""
        game = Game.objects.create(
            name=orig_value['name'],
            url=orig_value['url'],
            price=orig_value['price'],
            description=orig_value['description'],
        )
        self.assertIsInstance(game, Game)
        self.assertEqual(game.__str__(), game.name)

    def test_games_can_be_updated(self):
        """Create a game, update fields, refresh from db and assert."""
        # create the instance with initial values
        game_0 = Game.objects.create(
            name=orig_value['name'],
            url=orig_value['url'],
            price=orig_value['price'],
            description=orig_value['description'],
        )
        # update the values and save
        game_0.name = new_value['name']
        game_0.url = new_value['url']
        game_0.price = new_value['price']
        game_0.description = new_value['description']
        game_0.save()
        # Refresh the instance with the one from database
        game_0.refresh_from_db()
        # Assert each field
        self.assertEqual(game_0.__str__(), new_value['name'])
        self.assertEqual(game_0.url, new_value['url'])
        self.assertEqual(game_0.price, Decimal(new_value['price']).quantize(TWOPLACES))
        self.assertEqual(game_0.description, new_value['description'])

    def test_games_can_have_grade(self):
        """Games that have grade can be identified"""
        self.with_grade.refresh_from_db()
        self.assertEqual(self.no_grade.grade, None, msg='Grade should not have value.')
        self.assertEqual(self.with_grade.grade, 5, msg='Grade should have value.')

    def test_games_grade_is_average(self):
        """Games that have grade, will have average"""
        # Create another review
        Review.objects.create(
            game=self.with_grade,
            created_by=self.user_1.profile,
            grade=3,
        )
        # Get data again
        self.assertEqual(self.with_grade.grade, 4, msg='Grade is average.')
