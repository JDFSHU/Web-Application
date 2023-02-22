from django.shortcuts import render, redirect, get_object_or_404 
from .models import Event, Review, Sale
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # For the Content Management System (CMS)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # For the Content Management System (CMS)
from .forms import ContactForm, ReviewForm, EventForm, SaleForm 
from django.contrib.auth.models import User
from django.core.mail import send_mail # For the Contact Us form
from django.conf import settings # For the Contact Us form
from django.contrib import messages # For the Content Management System (CMS)
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView


# These views map to the paths in the events app urls.py file
def home(request):
    return render(request, 'events/home.html') # render the home.html template when requested

def events(request):
    context = {
        'events': Event.objects.all(),
    }
    return render(request, 'events/events.html', context) # render the events.html template when requested

def reviews(request):
    return render(request, 'events/reviews.html') # render the reviews.html template when requested


def about(request):
    return render(request, 'events/about.html') # render the about.html template when requested

def contact(request):
    return render(request, 'events/contact.html') # render the contact.html template when requested

def upload(request): # This view is used to upload contact us form data to the database and sends an email to the admin
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent! Thank you for contacting us, we will get back to you as soon as possible.')
            send_mail(
                'New Contact Form Submission',
                'A new contact form has been submitted on your website.',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        return redirect('events-home')
    return render(request, 'events/contact_form.html', {'form' : ContactForm})

# This view is used to request the search_events template and return the search results
def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        search_events = Event.objects.filter(
            Q(name__icontains=searched) | 
            Q(location__icontains=searched) | 
            Q(event_type__icontains=searched)
        )
        return render(request, 'events/search_events.html', {'searched': searched, 'search_events': search_events})
    else:
        return render(request, 'events/search_events.html', {'searched': '', 'search_events': []})


def not_admin(request): # This view is for the not_admin rights error page
    return render(request, 'events/not_admin.html') # render the not_admin.html template when requested

def not_author(request): # This view is for the not_author rights error page
    return render(request, 'events/not_author.html') # render the not_admin.html template when requested

# This classed based view is for the buy tickets form which allows the user to purchase tickets for an specific event
class BuyTicketsView(FormView):
    model = Sale
    template_name = 'events/buy_tickets.html'
    form_class = SaleForm
    success_url = '/events/'

    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.kwargs['pk'])
        form.save()
        email = form.instance.email # gets the email from the form
        messages.success(self.request, 'Your tickets have been purchased, You will receive a confirmation email shortly.')
        # sends an email to the user with a message saying the tickets will be sent seperately soon
        send_mail(
                'Your Tickets will be on the way soon!',
                'Thank you for your purchase, your requested purchase will be on the way to your email address soon.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url



# Start of ADMIN Content Management System (CMS) views to add/update/delete Events

class EventsListView(ListView): # This view is used to display all the events in the database
    model = Event # Tells the view which model to query
    template_name = 'events/events.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'events' # name of the object list that will be used in the template

class EventsDetailView(DetailView): # This view is used to display the details of a single event
    model = Event # Tells the view which model to query


class EventsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView): # LoginRequiredMixin is used to prevent users from creating events without logging in
    model = Event # Tells the view which model to query
    form_class = EventForm

    # test_func part of UserPassesTestMixin, checks to see if the user is admin or not, if not 403 forbidden error is returned
    def test_func(self):
        if self.request.user.username == 'admin':
            return True
        return False
    
    def handle_no_permission(self): # redirects to the not_admin page if the test_func returns false
        return redirect('not-admin')
    


class EventsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # LoginRequiredMixin is used to prevent users from updating events without logging in
    model = Event # Tells the view which model to query
    form_class = EventForm

    # checks to see if the user is admin or not, if not 403 forbidden error is returned
    def form_valid(self, form):
        if self.request.user.username == 'admin':
            form.instance.user = self.request.user
            return super().form_valid(form)
        
    # test_func part of UserPassesTestMixin, checks to see if the user is admin or not, if not 403 forbidden error is returned
    def test_func(self):
        if self.request.user.username == 'admin':
            return True
        return False
    
    def handle_no_permission(self): # redirects to the not_admin page if the test_func returns false
        return redirect('not-admin')


class EventsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event # Tells the view which model to query
    success_url = '/events/' # redirect to the events page after deleting an event

    # test_func part of UserPassesTestMixin, checks to see if the user is admin or not, if not 403 forbidden error is returned
    def test_func(self):
        if self.request.user.username == 'admin':
            return True
        return False
    
    def handle_no_permission(self): # redirects to the not_admin page if the test_func returns false
        return redirect('not-admin')

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
    
    def handle_no_permission(self): # redirects to the not_author page if the test_func returns false
        return redirect('not-author')

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review # Tells the view which model to query
    success_url = '/reviews/' # redirect to the reviews page after deleting a review
    
    def test_func(self):
        review = self.get_object()
        if self.request.user.username == review.author:
            return True
        return False
    
    def handle_no_permission(self): # redirects to the not_author page if the test_func returns false
        return redirect('not-author')

# End of USER Content Management System (CMS) views to add/update/delete Reviews

