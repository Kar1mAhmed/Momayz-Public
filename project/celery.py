from __future__ import absolute_import, unicode_literals

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

import os
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Africa/Cairo')

app.config_from_object(settings, namespace='CELERY')


app.conf.beat_schedule = {
    'flight_notification': {
        'task': 'settings.tasks.flight_notification',
        'schedule': crontab(minute='*/30', hour='6-18')
    },
    
    'midnight_run': {
        'task': 'settings.tasks.midnight',
        'schedule': crontab(minute=0, hour=0)
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def notfiy(self, fcm_url, payload, headers):
    requests.post(fcm_url, json=payload, headers=headers)