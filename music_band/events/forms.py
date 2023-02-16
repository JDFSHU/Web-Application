from django.forms import ModelForm
from django import forms
from .models import ContactFormData, Review
from django.core.validators import MinValueValidator, MaxValueValidator


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormData
        fields = ['name', 'email', 'subject', 'message']

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

        