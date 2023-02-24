from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from PIL import Image
from django.core.exceptions import ValidationError

# Main Model for the events app, this model is used to store all the data for the events and the other models have primary keys that reference this model
class Event(models.Model):
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()
    photo = models.ImageField(upload_to='imgs')

    def __str__(self): # this method is used to return the name of the event when it is called which is used in the admin backend
        return self.name

    def get_absolute_url(self): # this method is used to return the url to a specific event detail page
        return reverse('event-detail', kwargs={'pk': self.pk}) # return the url to a specific event detail page


# This Model is used to allow users to review events, foreign keys are used to reference the event and user models
class Review(models.Model):
    author = models.CharField(max_length=100)
    event_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)]) # event rating is a positive small integer field
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self): # this method is used to return the name of the event when it is called which is used in the admin backend
        return self.author
    
    def get_absolute_url(self): 
        return reverse("review-detail", kwargs={"pk": self.pk})


# This Model is used to store the data from the contact form, please note that an email is also sent to the admins email address when a contact form is submitted
class ContactFormData(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): # this method is used to return the name of the event when it is called which is used in the admin backend
        return self.name


# This function is used to validate the card code the user provides, it must be 3 digits long, otherwise it will raise a validation error
def validate_card_code(code):
    if len("{:03d}".format(code)) != 3: # this line of code is used to format the code to 3 digits long AND accept a code with digits that begin with 0
        raise ValidationError('Code must be 3 digits long')

# This function is used to validate the card number the user provides, it must be 16 digits long, otherwise it will raise a validation error   
def validate_card_number(card_number):
    if len(str(card_number)) != 16:
        raise ValidationError('Card number must be 16 digits long')

# This Model is used to store the data from the sale form, please note that an email is also sent to the buyers email address when a sale form is submitted
# Foreign keys are used to reference the event model
class Sale(models.Model):
    name_on_card = models.CharField(max_length=64)
    email = models.EmailField(default='c1004433@exchange.shu.ac.uk') # this field is set to my email address for testing purposes
    card_number = models.PositiveBigIntegerField(default='1234123412341234', validators=[validate_card_number]) # this field is validated using the validate_card_number function
    code = models.PositiveSmallIntegerField(default='123', validators=[validate_card_code]) # this field is validated using the validate_card_code function
    expiry_date = models.DateField(default='2021-01-01') # this field is set to a default date for testing purposes
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    
    def __str__(self): # this method is used to return the name of the card holder when it is called which is used in the admin backend
        return f"{self.name_on_card}'s purchase"