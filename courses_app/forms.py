from django.forms import ModelForm, DateTimeInput

from courses_app.models import Course


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["name", "description", "start_date", "end_date"]
        widgets = {
            "start_date": DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": DateTimeInput(attrs={"type": "datetime-local"}),
        }
