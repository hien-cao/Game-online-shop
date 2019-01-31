from django.contrib.auth.models import User

# Some generic variables
base_username = 'mock_user_'
mock_domain = '@mock.com'
password = 'foobarbaz123'


def create_mock_user(index=0, **extra_fields):
    return User.objects.create_user(
        '{0}{1}'.format(base_username, index),
        email='{0}{1}{2}'.format(base_username, index, mock_domain),
        password=password,
        **extra_fields
    )
