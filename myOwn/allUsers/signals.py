# corey Schafer
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# if there is a sender, that's gonna be the user
# when the user is saved, send this post_save signal
# and this signal is going to be received by the receiver; the receiver is the create_profile function
# this function takes arguements from the post_save signal
# in this function, if an user is created, then create a profile


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
# this saves the profile every time the user is saved