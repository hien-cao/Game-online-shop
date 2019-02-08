from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Profile model to provide additional properties to Djangos abstract user
    model
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    # Profile.is_developer has to be true for the user to be able to
    # add games and access dev api
    is_developer = models.BooleanField(default=False)
    # Separate field to track email confirmation status. Even though the
    # Django user model provides 'active' property, we may want to be able
    # to deactivate accounts (banning) even though their emails will remain
    # confirmed
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:  # Create profile for user when user is created
            Profile.objects.create(user=instance)

    # whenever a user instance is saved, will also save profile linked to it
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
