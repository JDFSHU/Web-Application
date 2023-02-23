from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views # imports the views from the users app
from django.contrib.auth import views as auth_views # imports the views from the auth app


urlpatterns = [

    path('', include('events.urls')), # '' Maps the home page of the site to the events app
    path('admin/', admin.site.urls), # Admin Path

    # Registration, Login, Logout, delete_user and Profile Paths
    path('register/', user_views.register, name='register'), # maps the register page to the register view
    path('login/' , auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), # maps the login page to the login view
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'), # maps the logout page to the logout view
    path('profile/', user_views.profile, name='profile'), # maps the profile page to the profile view
    path('delete_user/', user_views.delete_user, name='delete'), # maps the delete_user page to the delete_user view


    # Password Reset Functionality Paths
    path('password-reset/', 
    auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
    name='password_reset'), # maps password-reset/ to the PasswordResetView class in the auth_views module

    path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
    name='password_reset_done'), # maps password-reset/done/ to the PasswordResetDoneView class in the auth_views module

    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
    name='password_reset_confirm'), # maps password-reset-confirm/<uidb64>/<token>/ to the PasswordResetConfirmView class in the auth_views module

    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
    name='password_reset_complete'), # maps password-reset-complete/ to the PasswordResetCompleteView class in the auth_views module
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # adds the media url and media root to the urlpatterns list