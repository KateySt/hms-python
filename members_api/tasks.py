from datetime import date
from celery import shared_task

@shared_task
def send_birthday_notifications():
    from django.contrib.auth import get_user_model
    from notifications_app.models import Notification

    User = get_user_model()

    today = date.today()
    users = User.objects.filter(is_active=True, date_of_birth__isnull=False)

    for user in users:
        if user.date_of_birth.month == today.month and user.date_of_birth.day == today.day:
            notification_exists = Notification.objects.filter(
                member=user,
                title='Happy Birthday!',
                created_at__year=today.year,
                created_at__month=today.month,
                created_at__day=today.day
            ).exists()

            if not notification_exists:
                Notification.objects.create(
                    member=user,
                    title='Happy Birthday!',
                    message=f'Wish you a happy birthday, {user.full_name()}!',
                )
