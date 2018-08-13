import os
from celery import Celery
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = "authors.settings"

app = Celery('authors')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks([a for a in settings.INSTALLED_APPS])
