import os
from celery import Celery

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery
app = Celery('config')

# Загружаем конфигурацию из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()