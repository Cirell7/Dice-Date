import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from celery import current_app
print("BROKER_URL:", current_app.conf.broker_url)
print("RESULT_BACKEND:", current_app.conf.result_backend)