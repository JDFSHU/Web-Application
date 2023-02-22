from django.contrib import admin
from .models import Profile

# Registering models in the admin backend
admin.site.register(Profile)