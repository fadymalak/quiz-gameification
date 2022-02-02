import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_gameification.settings')

app = Celery('quiz_gameification')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()