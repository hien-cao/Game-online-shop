# Generated by Django 2.1.3 on 2019-02-05 16:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_remove_profile_games'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='apikey', to='user.Profile')),
            ],
        ),
    ]
