from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

# Celery Setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Fampay.settings")

app = Celery("Fampay")
app.conf.enable_utc = False

app.conf.update(timezone="Asia/Kolkata")

app.config_from_object(settings, namespace="CELERY")

# Celery Beat Settings
# Scheduled task to fetch videos in interval of 60 seconds asynchronously and save in DB.
app.conf.beat_schedule = {
    "fetch-videos-10": {
        "task": "youtube.scheduled_task.fetch_yt_videos",
        "schedule": 60.0,
    }
}

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
