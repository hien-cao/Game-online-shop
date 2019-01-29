from django.test import TestCase

from ..game import Game
from ....review.models import Review

from ....user.utils.mock_user import create_mock_user


fields = ["name", "description", "url", "price"]
orig_value = {
    "name": "game_0",
    "description": "foo",
    "url": "https://localhost:7999/",
    "price": 0
}
new_value = {
    "name": "game_1",
    "description": "bar",
    "url": "https://localhost:7998/",
    "price": 0.01
}


class GameTestCase(TestCase):
    user_0, user_1 = (None, None)
    no_grade, with_grade = (None, None)

    def setUp(self):
        # Create object without reviews
        self.no_grade = Game.objects.create(
            name="no_grade",
            url="https://localhost:8000/",
            price=0,
        )
        # Create some mock users
        self.user_0 = create_mock_user()
        self.user_1 = create_mock_user(1)
        # Create object with reviews
        self.with_grade = Game.objects.create(
            name="with_grade",
            url="https://localhost:8001/",
            price=0,
        )
        # Create mock review
        Review.objects.create(
            game=self.with_grade,
            created_by=self.user_0.profile,
            grade=5,
        )

    def test_games_can_be_created(self):
        game_0 = Game.objects.create(
            name=orig_value["name"],
            url=orig_value["url"],
            price=orig_value["price"],
            description=orig_value["description"],
        )
        self.assertTrue(isinstance(game_0, Game))
        self.assertEqual(game_0.__str__(), game_0.name)

    def test_games_can_be_updated(self):
        game_0 = Game.objects.create(
            name=orig_value["name"],
            url=orig_value["url"],
            price=orig_value["price"],
            description=orig_value["description"],
        )
        for field in fields:
            setattr(game_0, field, new_value[field])
            self.assertEqual(game_0[field], new_value[field])
            setattr(game_0, field, orig_value[field])
            self.assertEqual(game_0[field], orig_value[field])

    def test_games_can_have_grade(self):
        """Games that have grade can be identified"""
        self.assertEqual(self.no_grade.grade, None, msg="Grade should not have value.")
        self.assertEqual(self.with_grade.grade, 5, msg="Grade should have value.")

    def test_games_grade_is_average(self):
        """Games that have grade, will have average"""
        # Create another review
        Review.objects.create(
            game=self.with_grade,
            created_by=self.user_1.profile,
            grade=3,
        )
        # Get data again
        self.assertEqual(self.with_grade.grade, 4, msg="Grade is average.")
