from django.db import models

class Category(models.Model):
    label = models.CharField(max_length=32, unique=True)
