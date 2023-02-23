from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required # import the login_required decorator which makes sure that a user is logged in before accessing the profile page
from django.core.mail import send_mail
from django.conf import settings

@login_required #  login required decorator restricts access to the view to logged in users
def profile(request):
    if request.method == 'POST':
        # creates a form with the data from the current user and populates the fields with the data from the current user
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        # creates a form with the data from the current user's profile and populates the fields with the data from the profile
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid(): # checks if the forms are valid
            user_update_form.save() # saves the form to the database
            profile_update_form.save() # saves the form to the database
            messages.success(request, f'Account Updated!') # displays a success message to the user using the messages module
            return redirect('profile') # redirects the user to the profile page
    else:
        user_update_form = UserUpdateForm(instance=request.user) # creates a form with the data from the current user and populates the fields with the data from the current user
        profile_update_form = ProfileUpdateForm(instance=request.user.profile) # creates a form with the data from the current user's profile and populates the fields with the data from the profile

    
    form_dict = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }
    return render(request, 'users/profile.html', form_dict) # renders the profile.html template


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # create a form instance and populate it with data from the request:
        if form.is_valid(): # if the form is valid
            form.save() # save the user
            uname = form.cleaned_data.get('username') # get the username from the form
            email = form.cleaned_data.get('email') # get the email from the form
            messages.success(request, f'Account created for {uname}, You can now login!') # display a success message
            send_mail(
                'Music Band Account Registration',
                'Thank you for registering with Music Band. You can now login to your account and start using the app.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('login') # redirect to loin page after successful registration
            
    else: # if the form is not valid, display the form again
        form = RegistrationForm() # create a blank form
    return render(request, 'users/register.html', {'form': form})


@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, f'Account Deleted!') # displays a success message to the user using the messages module
        return redirect('register') # redirects the user to the register page
    return render(request, 'users/user_confirm_delete.html')