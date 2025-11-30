import os
from celery import Celery

# ИСПРАВЬ ЭТУ СТРОКУ!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()