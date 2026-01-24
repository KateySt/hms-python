from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from courses_app.models import Course

SUPPORTED_LANGUAGES = [
    ('en', _('English')),
    ('uk', _('Ukraine')),
]

GANDER = [
    ('male', _('Male')),
    ('female', _('Female')),
    ('other', _('Other'))
]


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('The Phone field must be set'))
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, email, password, **extra_fields)


class Member(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last name"))
    phone = models.CharField(max_length=20, unique=True, verbose_name=_("Phone"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Date of birth"))

    image = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_("Image"),
        help_text=_("Path to image in S3 storage")
    )

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("Date joined"))
    last_login = models.DateTimeField(auto_now=True, verbose_name=_("Date of last login"))

    gender = models.CharField(max_length=10, choices=GANDER, default='other', verbose_name=_("Gender"))
    language = models.CharField(max_length=10, choices=SUPPORTED_LANGUAGES, default='en', verbose_name=_("Language"))

    color = models.CharField(max_length=7, default='#000000', verbose_name=_("Color"))

    is_superuser = models.BooleanField(default=False, verbose_name=_("Superuser"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Staff"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))

    courses = models.ManyToManyField(Course, related_name='members', verbose_name=_("Courses"))

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')
        permissions = (
            ('can_add_courses', _('Can add courses')),
            ('can_edit_courses', _('Can edit courses')),
            ('can_delete_courses', _('Can delete courses')),
        )

    def __str__(self):
        return f"{self.phone} ({self.email})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
