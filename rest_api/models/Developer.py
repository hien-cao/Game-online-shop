from django.db import models
from django.contrib.auth.models import User

class Developer(models.Model):
    user = models.OneToOneField(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        primary_key=True
    )
    is_developer = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
