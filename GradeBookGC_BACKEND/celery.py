import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GradeBookGC_BACKEND.settings')

app = Celery('GradeBookGC_BACKEND')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
