from django.urls import path
from .views import EventsListView, EventsDetailView, EventsCreateView, EventsUpdateView, EventsDeleteView
from .views import ReviewListView, ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView
from .views import UserReviewListView
from . import views # import views.py file from the same directory

# Create a list of paths which map to the views in views.py
urlpatterns = [
    path('', views.home, name='events-home'), # '' means empty route which maps to the home page, the name = is used to reference the path in the html files

    path('events/', EventsListView.as_view(), name='events-events'), # 'events/' maps to the events page
    path('events/<int:pk>/', EventsDetailView.as_view(), name='event-detail'), # 'events/<int:pk>/' maps to the event detail page
    path('events/new/', EventsCreateView.as_view(), name='event-create'), # 'events/new/' maps to the event create page
    path('events/<int:pk>/update/', EventsUpdateView.as_view(), name='event-update'), # 'events/<int:pk>/update/' maps to the event update page
    path('events/<int:pk>/delete/', EventsDeleteView.as_view(), name='event-delete'), # 'events/<int:pk>/delete/' maps to the event delete page
    
    path('reviews/', ReviewListView.as_view(), name='events-reviews'), # 'reviews/' maps to the reviews page
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/new/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('user/<str:username>', UserReviewListView.as_view(), name='user-reviews'),

    path('about/', views.about, name='events-about'), # 'about/' maps to the about us page

    path('contact/', views.contact, name='events-contact'), # 'contact/' maps to the contact us page
    path('contact/upload', views.upload, name='events-contact-upload'),
]
