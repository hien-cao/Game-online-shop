from django.db import models

from ...user.models import Profile

class Game(models.Model):
    name = models.CharField(unique=True, max_length=128)
    description = models.TextField()
    url = models.URLField(unique=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    created_at = models.DateField(
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='tags',
        blank=True
    )

    def __str__(self):
        return self.name
