from django.urls import path

from members_app.views import get_me, edit_me, remove_course_from_member

urlpatterns = [
    path('', get_me, name='get_me'),
    path('edit/', edit_me, name='edit_me'),
    path('remove_course/<int:course_id>/', remove_course_from_member, name='remove_course_from_member'),
]
