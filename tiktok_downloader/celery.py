
# celery.py
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiktok_downloader.settings')

# Create Celery application
app = Celery('tiktok_downloader')

# Load settings from Django settings file with 'CELERY_' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Celery: Request: {self.request!r}")
