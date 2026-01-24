from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Notification(models.Model):
    title = models.CharField(
        max_length=255, verbose_name=_("Title"), help_text=_("Notification title")
    )
    message = models.TextField(
        verbose_name=_("Message"), help_text=_("Notification message content")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
        help_text=_("Date and time when notification was created"),
    )
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Member"),
        help_text=_("User who receives this notification"),
    )

    def __str__(self):
        return f"{self.title} - {self.member.phone}"

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]
