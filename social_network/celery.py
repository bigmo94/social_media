from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')
app = Celery('social_network')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_news_every_day': {
        'task': 'send_news',
        'schedule': crontab(minute='*/1'),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
