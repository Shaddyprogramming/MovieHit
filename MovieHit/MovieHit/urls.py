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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('account/', views.account, name='account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('update_email/', views.update_email, name='update_email'),
    path('update_email/<uidb64>/<token>/<str:new_email_b64>/', views.email_update_confirm, name='email_update_confirm'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('movie/<str:movie_id>/', views.movie_detail, name='movie_detail'),

]

if settings.DEBUG:
    # Use Django's static() helper for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Use our custom view for production
    urlpatterns += [
        path('media/<path:path>', views.serve_media, name='serve_media'),
    ]