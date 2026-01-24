from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver, Signal

from notifications_app.models import Notification

member_changed = Signal()

User = get_user_model()


@receiver(user_logged_in)
def send_birthday_notification(sender, request, user, **kwargs):
    today = date.today()
    notification_exists = Notification.objects.filter(
        member=user, title="Happy Birthday!", created_at__year=today.year
    ).exists()
    if (
        user.date_of_birth
        and user.date_of_birth.month == today.month
        and user.date_of_birth.day == today.day
    ):
        if not notification_exists:
            Notification.objects.create(
                member=user,
                title="Happy Birthday!",
                message="Wish you a happy birthday!",
            )


@receiver(pre_save, sender=User)
def send_new_user_notification(sender, instance, **kwargs):
    users = User.objects.exclude(id=instance.id)
    for u in users:
        Notification.objects.create(
            member=u,
            title="Added new user!",
            message=f"{instance.first_name} {instance.last_name} was added!",
        )


@receiver(post_delete, sender=User)
def send_user_deleted_notification(sender, instance, **kwargs):
    users = User.objects.exclude(id=instance.id)
    for u in users:
        Notification.objects.create(
            member=u,
            title="Deleted user!",
            message=f"{instance.first_name} {instance.last_name} was deleted!",
        )


@receiver(member_changed)
def notify_status_change(sender, member, changed_fields, **kwargs):
    Notification.objects.create(
        member=member,
        title="Status changed",
        message=f"Fields {', '.join(changed_fields)} were updated.",
    )
