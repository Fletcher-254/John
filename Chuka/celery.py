import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chuka.settings')

app = Celery('Chuka')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()