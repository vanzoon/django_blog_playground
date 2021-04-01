import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogengine.settings')

app = Celery('send_email')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery beat tasks

app.conf.beat_schedule = {
    'send_bullshit_every_5_min': {
        'task': 'send_email.tasks.send_bullshit_email',
        'schedule': crontab(minute='*/5')
    }
}
