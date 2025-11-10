from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from courses_app.forms import CourseForm
from courses_app.models import Course
from members_app.models import Member


@login_required
def all_courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_courses')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})


@login_required
def edit_course(request, course_id):
    member = get_object_or_404(Member, user=request.user)
    course = get_object_or_404(Course, id=course_id, members=member)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('all_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})
