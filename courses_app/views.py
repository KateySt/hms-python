from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from courses_app.forms import CourseForm
from courses_app.models import Course


class AllCoursesView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses'


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    permission_required = 'members_app.can_add_courses'
    success_url = reverse_lazy('all_courses')


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    permission_required = 'members_app.can_edit_courses'
    success_url = reverse_lazy('all_courses')

    def get_object(self, queryset=None):
        member = self.request.user
        course_id = self.kwargs.get('course_id')
        return get_object_or_404(Course, id=course_id, members=member)
