from django.test import TestCase

from .utils.mock_user import create_mock_user

from .models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = create_mock_user(0)

    def test_profile_is_created_when_user_is(self):
        """profile can be created"""
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_can_be_updated(self):
        """profile can be updated on its own"""
        self.user.profile.is_developer = True
        self.user.profile.save()
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.is_developer)

    def test_profile_is_saved_when_user_is(self):
        """profile is saved when user is"""
        self.user.profile.is_developer = True
        self.user.save()
        self.user.refresh_from_db()
        self.assertTrue(self.user.profile.is_developer)

    def test_profile_is_deleted_when_user_is(self):
        """profile should be deleted when user is"""
        self.user.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(user=self.user)

    def test_profile__str__(self):
        """__str__() method should return username"""
        username = '{0}'.format(self.user.profile)
        self.assertEqual(self.user.username, username)
