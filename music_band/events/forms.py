from django.forms import ModelForm
from django import forms
from .models import ContactFormData, Review, Event, Sale
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


# Each of these custom forms are used for a user to submit data to the database to the relevant models

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormData
        fields = ['name', 'email', 'subject', 'message']

# This form allows the admin to submit a new event to the database, the widgets are used to change the input type of the date field to a drop down box
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['photo', 'name', 'event_type', 'location', 'date', 'description']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReviewForm(forms.ModelForm):
    event_rating = forms.IntegerField(
        label='Rating',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    class Meta:
        model = Review
        fields = ['event', 'event_rating', 'content']


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['name_on_card', 'email', 'card_number', 'code', 'expiry_date']
        widgets = {
            'event': forms.HiddenInput(),
            'expiry_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }
