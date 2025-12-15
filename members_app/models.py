from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from courses_app.models import Course

SUPPORTED_LANGUAGES = [
    ('en', 'English'),
    ('uk', 'Ukraine'),
]

GANDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
]


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        if not email:
            raise ValueError('The Email field must be set')
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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True, verbose_name="Phone")
    email = models.EmailField(unique=True, verbose_name="Email")
    date_of_birth = models.DateField(null=True, blank=True)

    image = models.ImageField(upload_to='members/images', null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date joined")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Date of last login")

    gender = models.CharField(max_length=10, choices=GANDER, default='other')
    language = models.CharField(max_length=10, choices=SUPPORTED_LANGUAGES, default='en')

    color = models.CharField(max_length=7, default='#000000')

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    courses = models.ManyToManyField(Course, related_name='members')

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        permissions = (
            ('can_add_courses', 'Can add courses'),
            ('can_edit_courses', 'Can edit courses'),
            ('can_delete_courses', 'Can delete courses'),
        )

    def __str__(self):
        return f"{self.phone} ({self.email})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
