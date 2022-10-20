from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nordigen_api.settings')

app = Celery('nordigen_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()