from django.contrib import admin
from .models import Profile

# This is so that the Profile model can be viewed in the admin panel
admin.site.register(Profile)