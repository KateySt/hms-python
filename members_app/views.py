from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from courses_app.models import Course
from members_app.forms import MemberForm

User = get_user_model()


@login_required
def get_me(request):
    return render(request, 'profile.html', {'member': request.user})


@login_required
def edit_me(request):
    member = request.user
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            form.save_m2m()
            if form.changed_data:
                from members_app.signals import member_changed
                member_changed.send(sender=User, member=member, changed_fields=form.changed_data)

            return redirect('get_me')
    else:
        form = MemberForm(instance=member)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
@permission_required('members_app.can_delete_courses', raise_exception=True)
def remove_course_from_member(request, course_id):
    member = request.user
    course = get_object_or_404(Course, id=course_id)

    member.courses.remove(course)

    return redirect('get_me')
