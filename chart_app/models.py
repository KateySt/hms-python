from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Message(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Member"))
    message = models.TextField(verbose_name=_("Message"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
