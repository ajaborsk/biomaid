"""
WSGI config for dra project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dra.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dem.settings.production')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

application = get_wsgi_application()
