from django.shortcuts import render, redirect, get_object_or_404 
from .models import Event, Review
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # For the Content Management System (CMS)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # For the Content Management System (CMS)
from .forms import ContactForm, ReviewForm 
from django.contrib.auth.models import User
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

def reviews(request):
    return render(request, 'events/reviews.html', {'title': 'Reviews'}) # render the reviews.html template when requested


def about(request):
    return render(request, 'events/about.html', {'title': 'About Us'}) # render the about.html template when requested

def contact(request):
    return render(request, 'events/contact.html', {'title': 'Contact Us'}) # render the contact.html template when requested

def upload(request): # This view is used to upload contact us form data to the database
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent! Thank you for contacting us, we will get back to you as soon as possible.')
        return redirect('events-home')
    return render(request, 'events/contact_form.html', {'form' : ContactForm}) 

# Start of ADMIN Content Management System (CMS) views to add/update/delete Events

class EventsListView(ListView): # This view is used to display all the events in the database
    model = Event # Tells the view which model to query
    template_name = 'events/events.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'events' # name of the object list that will be used in the template

class EventsDetailView(DetailView): # This view is used to display the details of a single event
    model = Event # Tells the view which model to query


class EventsCreateView(LoginRequiredMixin, CreateView): # LoginRequiredMixin is used to prevent users from creating events without logging in
    model = Event # Tells the view which model to query
    fields = ['photo', 'name', 'event_type', 'location', 'date', 'description'] # fields that will be displayed in the form

    # checks to see if the user is admin or not, if not they are returned to the homepage, only the admin can create events
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.username != 'admin':
            return redirect('events-home') # redirect to home page
        return super().dispatch(request, *args, **kwargs)

class EventsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # LoginRequiredMixin is used to prevent users from updating events without logging in
    model = Event # Tells the view which model to query
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
    model = Event # Tells the view which model to query
    success_url = '/events/' # redirect to the events page after deleting an event

    def test_func(self):
        if self.request.user.username == 'admin':
            return True
        return False

# End of ADMIN Content Management System (CMS) views to add/update/delete Events

# Start of USER Content Management System (CMS) views to add/update/delete Reviews

class ReviewListView(ListView): # This view is used to display all the reviews in the database
    model = Review # Tells the view which model to query
    template_name = 'events/reviews.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'reviews' # name of the object list that will be used in the template
    ordering = ['-date_posted'] # orders the reviews by date posted
    paginate_by = 5 # number of reviews to display per page

class UserReviewListView(ListView): # This view is used to display all the reviews in the database
    model = Review # Tells the view which model to query
    template_name = 'events/user_reviews.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'reviews' # name of the object list that will be used in the template
    paginate_by = 5 # number of reviews to display per page

    def get_queryset(self): 
        user = get_object_or_404(User, username=self.kwargs.get('username')) 
        return Review.objects.filter(author=user).order_by('-date_posted') # orders the reviews by date posted



class ReviewDetailView(DetailView): # This view is used to display the details of a single review
    model = Review # Tells the view which model to query

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review # Tells the view which model to query
    form_class = ReviewForm # Tells the view which custom form to use (allows min/max rating of 1-5)

    def form_valid(self, form): # sets the author to the current logged in user upon creating a new review
        form.instance.author = self.request.user
        return super().form_valid(form)

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review # Tells the view which model to query
    form_class = ReviewForm # Tells the view which custom form to use (allows min/max rating of 1-5)

    def form_valid(self, form):
        review = self.get_object()
        if self.request.user.username == review.author:
            form.instance.user = self.request.user
            return super().form_valid(form)
    
    def test_func(self):
        review = self.get_object()
        if self.request.user.username == review.author:
            return True
        return False

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review # Tells the view which model to query
    success_url = '/reviews/' # redirect to the reviews page after deleting a review
    
    def test_func(self):
        review = self.get_object()
        if self.request.user.username == review.author:
            return True
        return False


# End of USER Content Management System (CMS) views to add/update/delete Reviews

