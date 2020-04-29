"""
WSGI config for marshrutka project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'marshrutka.settings'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marshrutka.settings')
django.setup()
application = get_wsgi_application()
