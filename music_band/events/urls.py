from django.urls import path
from . import views
from .views import EventsListView, EventsDetailView, EventsCreateView, EventsUpdateView, EventsDeleteView, BuyTicketsView
from .views import ReviewListView, ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView, UserReviewListView


# Create a list of paths which map to the views in views.py
urlpatterns = [

    # Home Path
    path('', views.home, name='events-home'), # '' means empty route which maps to the home page, the name = is used to reference the path in the html files

    # Events Paths
    path('events/', EventsListView.as_view(), name='events-events'), # 'events/' maps to the events page
    path('events/<int:pk>/', EventsDetailView.as_view(), name='event-detail'), # 'events/<int:pk>/' maps to the event detail page
    path('events/new/', EventsCreateView.as_view(), name='event-create'), # 'events/new/' maps to the event create page
    path('events/<int:pk>/update/', EventsUpdateView.as_view(), name='event-update'), # 'events/<int:pk>/update/' maps to the event update page
    path('events/<int:pk>/delete/', EventsDeleteView.as_view(), name='event-delete'), # 'events/<int:pk>/delete/' maps to the event delete page
    path('events/<int:pk>/buy_tickets/', BuyTicketsView.as_view(), name='buy-tickets'), # 'events/buy_tickets/' maps to the buy tickets page
    
    # Reviews Paths
    path('reviews/', ReviewListView.as_view(), name='events-reviews'), 
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/new/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('user/<str:username>', UserReviewListView.as_view(), name='user-reviews'),

    # About Path
    path('about/', views.about, name='events-about'),

    # Contact Paths
    path('contact/', views.contact, name='events-contact'), 
    path('contact/upload', views.upload, name='events-contact-upload'),

    # Search Path
    path('search/', views.search_events, name='search-events'), 

    # 403 Error Paths
    path('not_admin/', views.not_admin, name='not-admin'),
    path('not_author/', views.not_author, name='not-author')
]
