from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class UTokenGenerator(PasswordResetTokenGenerator):
    """General token generator for users."""
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

# token generator for account activation
account_activation_token = UTokenGenerator()