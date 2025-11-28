from django.urls import path

from courses_app.views import AllCoursesView, CourseCreateView, CourseUpdateView

urlpatterns = [
    path('', AllCoursesView.as_view(), name='all_courses'),
    path('create/', CourseCreateView.as_view(), name='create_course'),
    path('edit/<int:course_id>', CourseUpdateView.as_view(), name='edit_course'),
]
