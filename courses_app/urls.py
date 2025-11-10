from django.urls import path

from courses_app.views import all_courses, create_course, edit_course

urlpatterns = [
    path('', all_courses, name='all_courses'),
    path('create/', create_course, name='create_course'),
    path('edit/<int:course_id>', edit_course, name='edit_course'),
]
