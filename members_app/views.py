from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from courses_app.models import Course
from members_app.forms import MemberForm
from members_app.models import Member


@login_required
def get_me(request):
    member = get_object_or_404(Member, user=request.user)
    return render(request, 'profile.html', {'member': member})


@login_required
def edit_me(request):
    member = get_object_or_404(Member, user=request.user)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            form.save_m2m()
            return redirect('get_me')
    else:
        form = MemberForm(instance=member)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def remove_course_from_member(request, course_id):
    member = get_object_or_404(Member, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    member.courses.remove(course)

    return redirect('get_me')
