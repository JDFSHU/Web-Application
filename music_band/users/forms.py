from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms.widgets import DateTimeInput

# Form that inherits from standard UserCreationForm and adds email field
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta: # this class is used to define the metadata of the model
        model = User # The model that this form will interact with
        fields = ['username', 'email', 'password1', 'password2'] # The fields that will be displayed in the form

# Form that updates the User Model
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email',]

# Form that updates the Profile Model
class ProfileUpdateForm(forms.ModelForm):
    dob = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Profile
        fields = [ 'full_name', 'dob', 'city_town', 'country', 'photo_of_user']

    # This function overides the default save method of the form to allow us to add a label to the dob field with the current dob of the user if it exists
    # This allows us to use both a drop-down date picker and a label with the current dob of the user to avoid confusion
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_dob = self.instance.dob.strftime('%d-%m-%Y') if self.instance.dob else ''
        self.fields['dob'].label = f"You're DOB is {current_dob}"
