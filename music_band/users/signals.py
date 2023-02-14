from django.db.models.signals import post_save # post_save is a signal that is sent after a model is saved
from django.contrib.auth.models import User # import the User model, sends the signal to the User model
from django.dispatch import receiver # receiver is a decorator that receives the signal and performs some task
from .models import Profile # import the Profile model

# This function = when a user is saved, send a signal to the Profile model to create a profile for the user
@receiver(post_save, sender=User) # receiver decorator, post_save is the signal, sender=User is the model that will receive the signal
def create_profile(sender, instance, created, **kwargs): # kwargs is a dictionary that contains all the keyword arguments that were passed to the function
    if created:
        Profile.objects.create(user=instance) # creates a profile for the user

@receiver(post_save, sender=User) # receiver decorator, post_save is the signal, sender=User is the model that will receive the signal
def save_profile(sender, instance, created, **kwargs): # kwargs is a dictionary that contains all the keyword arguments that were passed to the function
    instance.profile.save() # saves the profile