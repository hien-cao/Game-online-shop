import uuid

from django.db import models

from ...user.models import Profile


class ApiKey(models.Model):
    """
    ApiKey model for the Developer API.
    - key: UUIDField
    - owner: Profile
    """
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    owner = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='apikey'
    )

    def __str__(self):
        return str(self.key)
