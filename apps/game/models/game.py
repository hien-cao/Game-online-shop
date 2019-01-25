from django.db import models
from django.core.validators import MinValueValidator

from ...user.models import Profile


class Game(models.Model):
    name = models.CharField(unique=True, max_length=128)
    description = models.TextField(blank=True)
    url = models.URLField(unique=True)
    price = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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

    @property
    def grade(self):
        "Returns the grade calculated from reviews"
        reviews = self.reviews.all()
        for review in reviews:
            return round(float(sum(
                [review.grade for review in reviews]
            ) / len(reviews)), 2)
        return None

    def __str__(self):
        return self.name
