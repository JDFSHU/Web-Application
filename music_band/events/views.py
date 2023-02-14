from django.shortcuts import render, redirect
from .models import Event
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # For the Content Management System (CMS)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # For the Content Management System (CMS)
from .forms import ContactForm 
from django.contrib import messages # For the Content Management System (CMS)

# These views map to the paths in the events app urls.py file
def home(request):
    return render(request, 'events/home.html', {'title': 'Home'}) # render the home.html template when requested

def events(request):
    context = {
        'events': Event.objects.all(),
        'title': 'Events'
    }
    return render(request, 'events/events.html', context) # render the events.html template when requested

def about(request):
    return render(request, 'events/about.html', {'title': 'About Us'}) # render the about.html template when requested

def contact(request):
    return render(request, 'events/contact.html', {'title': 'Contact Us'}) # render the contact.html template when requested

def upload(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent! Thank you for contacting us, we will get back to you as soon as possible.')
        return redirect('events-home')
    return render(request, 'events/contact_form.html', {'form' : ContactForm}) 

# Start of Content Management System (CMS) views

class EventsListView(ListView):
    model = Event
    template_name = 'events/events.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'events'

class EventsDetailView(DetailView):
    model = Event

class EventsCreateView(LoginRequiredMixin, CreateView): # LoginRequiredMixin is used to prevent users from creating events without logging in
    model = Event
    fields = ['photo', 'name', 'event_type', 'location', 'date', 'description'] # fields that will be displayed in the form

    # checks to see if the user is admin or not, if not they are returned to the homepage, only the admin can create events
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.username != 'admin':
            return redirect('events-home') # redirect to home page
        return super().dispatch(request, *args, **kwargs)

class EventsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # LoginRequiredMixin is used to prevent users from updating events without logging in
    model = Event
    fields = ['photo', 'name', 'event_type', 'location', 'date', 'description'] # fields that will be displayed in the form

    # checks to see if the user is admin or not, if not 403 forbidden error is returned
    def form_valid(self, form):
        if self.request.user.username == 'admin':
            form.instance.user = self.request.user
            return super().form_valid(form)
    
    def test_func(self):
        if self.request.user.username == 'admin':
            return True
        return False

class EventsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/events/' # redirect to the events page after deleting an event

    def test_func(self):
        if self.request.user.username == 'admin':
            return True
        return False

# End of Content Management System (CMS) views

