from django.forms import ModelForm
from django import forms
from .models import ContactFormData, Review, Event
from django.core.validators import MinValueValidator, MaxValueValidator


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormData
        fields = ['name', 'email', 'subject', 'message']

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

        