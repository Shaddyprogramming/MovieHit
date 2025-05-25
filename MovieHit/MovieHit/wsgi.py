"""
WSGI config for MovieHit project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

For more information, visit
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os # Importing os module for interacting with the operating system
from django.core.wsgi import get_wsgi_application # Importing get_wsgi_application from Django's core WSGI module to create the WSGI application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', # Setting the default settings module for the Django application
    'MovieHit.settings') # 'MovieHit.settings' is the settings module for the MovieHit project

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application() # Creating the WSGI application object that can be used by WSGI servers
