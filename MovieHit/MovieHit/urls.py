"""
MovieHit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings #Importing settings from Django's configuration module
from django.conf.urls.static import static # Importing static helper for serving static files during development
from django.contrib import admin # Importing the admin module from Django's contrib package for the admin interface
from django.urls import path # Importing path function for defining URL patterns
from . import views # Importing views from the current package to handle requests
from django.contrib.auth.views import LogoutView # Importing LogoutView for handling user logout functionality


urlpatterns = [ # URL patterns for the MovieHit application
    path('admin/', admin.site.urls), # Admin interface URL
    path('', views.index, name='index'), # Home page URL, mapped to the index view
    path('signin/', views.signin, name='signin'), # Sign-in page URL, mapped to the signin view
    path('account/', views.account, name='account'), # User account page URL, mapped to the account view
    path('edit_profile/', views.edit_profile, name='edit_profile'), # Edit profile page URL, mapped to the edit_profile view
    path('password_reset/', views.password_reset, name='password_reset'), # Password reset page URL, mapped to the password_reset view
    path('password_reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'), # Password reset confirmation URL, mapped to the password_reset_confirm view
    path('update_email/', views.update_email, name='update_email'), # Update email page URL, mapped to the update_email view
    path('update_email/<uidb64>/<token>/<str:new_email_b64>/', views.email_update_confirm, name='email_update_confirm'), # Email update confirmation URL, mapped to the email_update_confirm view
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), # Logout URL, using Django's built-in LogoutView and redirecting to the home page after logout
    
    path('save_preference/', views.save_preference, name='save_preference'), # Save user preferences URL, mapped to the save_preference view
    path('movie/<str:movie_id>/', views.movie_detail, name='movie_detail'), # Movie detail page URL, mapped to the movie_detail view
    path('movie/<str:movie_id>/add_comment/', views.add_comment, name='add_comment'), # Add comment to movie URL, mapped to the add_comment view
    path('movie/<str:movie_id>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'), # Edit comment on movie URL, mapped to the edit_comment view
    path('movie/<str:movie_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'), # Delete comment on movie URL, mapped to the delete_comment view
]

if settings.DEBUG: # Check if the application is in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Serve media files during development using Django's static helper
else:
    urlpatterns += [ # Serve media files in production using a custom view
        path('media/<path:path>', views.serve_media, name='serve_media'), # Custom view to serve media files in production
    ]
