from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from PIL import Image

class Event(models.Model):
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()
    photo = models.ImageField(upload_to='')

    def __str__(self):
        return self.name

    def get_absolute_url(self): # this method is used to return the url to a specific event detail page
        return reverse('event-detail', kwargs={'pk': self.pk}) # return the url to a specific event detail page
    

class Review(models.Model):
    author = models.CharField(max_length=100)
    event_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)]) # event rating is a positive small integer field
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse("review-detail", kwargs={"pk": self.pk})
    


class ContactFormData(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name