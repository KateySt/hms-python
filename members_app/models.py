from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from courses_app.models import Course


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    courses = models.ManyToManyField(Course, related_name='members')
    phone = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=7, default='#000000')

    def __str__(self):
        return f"{self.user.username} ({self.user.email or "-"})"

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'


@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)
