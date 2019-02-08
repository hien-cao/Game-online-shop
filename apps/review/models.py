from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ..game.models import Game, Purchase
from ..user.models import Profile

rn = 'reviews'


class Review(models.Model):
    """ Model for the review of the game """
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name=rn
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name=rn
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    grade = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    content = models.TextField(
        blank=True
    )

    def save(self, *args, **kwargs):
        if Purchase.objects.filter(
            game=self.game,
            created_by=self.created_by,
            purchased_at__isnull=False
        ):
            super(Review, self).save(*args, **kwargs)

