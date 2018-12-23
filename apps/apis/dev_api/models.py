from django.db import models
import uuid

from ...user.models import Profile

class ApiKey(models.Model):
    key = models.CharField(
        max_length=128,
        unique=True,
        default=uuid.uuid4
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

    def generate(self):
        self.key = uuid.uuid4()

    def __str__(self):
        return self.key
