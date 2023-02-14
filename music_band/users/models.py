from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# This model is used to create a profile for each user which pulls from the default User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # OneToOneField used to link the user model to the profile model, if user is deleted the profile will be deleted too
    full_name = models.CharField(max_length=100, default='')
    dob = models.DateField(null=True, blank=True)
    city_town = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    photo_of_user = models.ImageField(default='default.jpg', upload_to='profile_pics') # uploads to /media/profile_pics or uses default.jpg if no image is uploaded

    def __str__(self):
        return f'{self.user.username} Profile' # example: admin Profile

    def save(self, *args, **kwargs): # overrides the save method
        super().save(*args, **kwargs) # calls the save method of the parent class

        img = Image.open(self.photo_of_user.path) # opens the image of the current instance

        if img.height > 250 or img.width > 250: # checks if the image is larger than 300px by 300px
            img_output = (250, 250) # sets the output size to 300px by 300px
            img.thumbnail(img_output) # resizes the image to the output size
            img.save(self.photo_of_user.path) # saves the image to the path of the current instance
