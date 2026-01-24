import factory
import pytz
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from faker import Faker

from courses_app.models import Course

fake = Faker()
User = get_user_model()
tz = pytz.timezone("UTC")


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course
        django_get_or_create = ("name",)

    name = factory.Faker("name")
    description = factory.Faker("text")
    start_date = factory.Faker("date")
    end_date = factory.Faker("date")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    phone = factory.Sequence(lambda n: f"+380671234{n:03}")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_of_birth = factory.Faker("date_of_birth")

    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def courses(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.courses.set(extracted)
        else:
            self.courses.add(CourseFactory())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "Test123!")
        user = super()._create(model_class, *args, **kwargs)
        user.set_password(password)
        user.save(update_fields=["password"])
        return user


class SupperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True


class DeletedUserFactory(UserFactory):
    is_deleted = True


class InactiveUserFactory(UserFactory):
    is_active = False
