# Generated by Django 2.1.3 on 2018-12-23 16:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKeys',
            fields=[
                ('key', models.CharField(default=uuid.uuid4, max_length=128, unique=True, editable=False, serialize=False)),
            ],
        ),
    ]
