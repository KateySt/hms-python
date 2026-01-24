from uuid import uuid4

from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from courses_app.models import Course
from members_app.boto_client import s3_bucket_service_factory
from members_app.forms import MemberForm, LoginForm, MemberCreateForm

User = get_user_model()


@login_required
def get_me(request):
    user = request.user

    if user.image:
        s3 = s3_bucket_service_factory()
        try:
            image_url = s3.get_file_url(user.image, expiration=3600)
            user.image = image_url
        except Exception as e:
            print(f"Error getting image URL: {e}")

    return render(request, "profile.html", {"member": request.user})


@login_required
def edit_me(request):
    member = request.user
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            form.save_m2m()
            if form.changed_data:
                from members_app.signals import member_changed

                member_changed.send(
                    sender=User, member=member, changed_fields=form.changed_data
                )

            return redirect("get_me")
    else:
        form = MemberForm(instance=member)
    return render(request, "edit_profile.html", {"form": form})


@login_required
@permission_required("members_app.can_delete_courses", raise_exception=True)
def remove_course_from_member(request, course_id):
    member = request.user
    course = get_object_or_404(Course, id=course_id)

    member.courses.remove(course)

    return redirect("get_me")


def register_view(request):
    if request.method == "POST":
        form = MemberCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])

            image = request.FILES.get("image_file")
            if image:
                try:
                    s3 = s3_bucket_service_factory()
                    file_extension = image.name.split(".")[-1]
                    file_name = f"{uuid4()}.{file_extension}"
                    prefix = f"avatars/user_{user.email}"

                    file_path = s3.upload_file_object(
                        prefix=prefix, source_file_name=file_name, content=image.read()
                    )
                    user.image = file_path

                except Exception as e:
                    print(request, f"Error uploading image: {str(e)}")

            user.save()
            form.save_m2m()

            login(request, user)
            print(request, "Account created successfully!")
            return redirect("get_me")
    else:
        form = MemberCreateForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]
            user = authenticate(username=phone, password=password)
            if user:
                login(request, user)
                return redirect("get_me")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
