from django.contrib import admin
from .models import Event, ContactFormData, Review, Sale

# This is so that the Event model can be viewed in the admin panel
admin.site.register(Event)
admin.site.register(ContactFormData)
admin.site.register(Review)
admin.site.register(Sale)
