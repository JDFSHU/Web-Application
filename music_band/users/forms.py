from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms.widgets import DateTimeInput

# this class inherits from UserCreationForm and adds an additional field for email
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta: # this class is used to define the metadata of the model
        model = User # the model that this form will interact with
        fields = ['username', 'email', 'password1', 'password2'] # the fields that will be displayed in the form

# Creating a form that updates our user model
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email',]

# Creating a form that updates our profile model
class ProfileUpdateForm(forms.ModelForm):
    dob = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = [ 'full_name', 'dob', 'city_town', 'country', 'photo_of_user']