from django.contrib import admin
from .models import Event, ContactFormData, Review, Sale

# Registering models in the admin backend
admin.site.register(Event)
admin.site.register(ContactFormData)
admin.site.register(Review)
admin.site.register(Sale)
