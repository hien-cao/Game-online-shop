# Generated by Django 2.1.3 on 2019-01-18 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20190118_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
