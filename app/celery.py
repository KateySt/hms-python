import os
import django
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from members_api.tasks import send_birthday_notifications  # noqa: F401

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()
app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.timezone = "UTC"

app.conf.beat_schedule = {
    "send-birthday-notifications-everyday": {
        "task": "members_api.tasks.send_birthday_notifications",
        "schedule": crontab(hour=8, minute=0),
    },
}
