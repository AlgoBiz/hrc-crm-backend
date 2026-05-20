import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrc_crm.settings')

app = Celery('hrc_crm')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'send-expiry-reminders-daily': {
        'task': 'user.tasks.send_expiry_reminders',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9:00 AM
    },
}

app.conf.timezone = 'Asia/Kolkata'
