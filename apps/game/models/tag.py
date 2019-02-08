from django.db import models


class Tag(models.Model):
    """
    Tag model.
    - name: CharField
    """
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name
