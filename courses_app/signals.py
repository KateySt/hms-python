from django.db.models.signals import pre_delete, m2m_changed, post_save
from django.dispatch import receiver

from courses_app.models import Course
from members_app.models import Member
from notifications_app.models import Notification


@receiver(pre_delete, sender=Course)
@receiver(post_save, sender=Course)
def send_course_notification(sender, instance, *args, **kwargs):
    signal = kwargs.get("signal")

    if signal == post_save:
        members_without_course = Member.objects.exclude(courses=instance)
        for member in members_without_course:
            Notification.objects.create(
                member=member,
                title="New course was created!",
                message=f"New course '{instance}' was created!",
            )
    else:
        members_with_course = instance.members.all()
        for member in members_with_course:
            Notification.objects.create(
                member=member,
                title="Course was deleted!",
                message=f"Course '{instance}' was deleted!",
            )


@receiver(m2m_changed, sender=Member.courses.through)
def notify_members_about_new_course(
    sender, instance, action, reverse, pk_set, **kwargs
):
    if action == "post_add":
        for course_id in pk_set:
            course = Course.objects.get(pk=course_id)
            members_to_notify = Member.objects.filter(courses=course)
            for member in members_to_notify:
                Notification.objects.create(
                    member=member,
                    title="New member joined the course!",
                    message=f"{instance.full_name()} joined the course '{course}'",
                )

    elif action == "pre_remove":
        for course_id in pk_set:
            course = Course.objects.get(pk=course_id)
            members_to_notify = Member.objects.filter(courses=course)
            for member in members_to_notify:
                Notification.objects.create(
                    member=member,
                    title="Member left the course!",
                    message=f"{instance.full_name()} left the course '{course}'",
                )
