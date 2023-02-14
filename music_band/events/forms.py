from django.forms import ModelForm
from django import forms
from .models import ContactFormData

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormData
        fields = ['name', 'email', 'subject', 'message']