from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
app = Celery('todo')
# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Autodiscover tasks from all installed apps.
app.autodiscover_tasks(settings.INSTALLED_APPS)