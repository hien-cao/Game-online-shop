from django.db import models

from ..user.models import Profile

class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

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
        on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='tags',
        blank=True
    )

    def __str__(self):
        return self.name

class Purchase(models.Model):
    purchased_at = models.DateField()
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )

class Save(models.Model):
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    content = models.TextField()

class Highscore(models.Model):
    score = models.IntegerField()
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
