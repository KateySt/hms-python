from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Permission
from django.forms import (
    ModelForm,
    TextInput,
    ColorInput,
    SelectMultiple,
    CheckboxSelectMultiple,
    Select,
    DateInput,
)

User = get_user_model()


class MemberForm(ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=CheckboxSelectMultiple(),
        required=False,
        label="Permissions",
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance", None)

        super().__init__(*args, **kwargs)

        permissions = Permission.objects.all().order_by(
            "content_type__app_label", "codename"
        )

        self.fields["user_permissions"].choices = [
            (perm.id, f"{perm.content_type.app_label}.{perm.codename} — {perm.name}")
            for perm in permissions
        ]

        if instance:
            self.fields["user_permissions"].initial = (
                instance.user_permissions.values_list("id", flat=True)
            )

    class Meta:
        model = User
        fields = [
            "phone",
            "color",
            "courses",
            "user_permissions",
            "gender",
            "language",
            "date_of_birth",
        ]
        widgets = {
            "phone": TextInput(attrs={"placeholder": "Enter phone"}),
            "color": ColorInput(),
            "courses": SelectMultiple(attrs={"size": 5}),
            "gender": Select(),
            "language": Select(),
            "date_of_birth": DateInput(attrs={"type": "date"}),
        }


class LoginForm(forms.Form):
    phone = forms.CharField(
        label="Phone",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Phone"}),
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        password = cleaned_data.get("password")

        if phone and password:
            user = authenticate(username=phone, password=password)
            if not user:
                raise forms.ValidationError("Invalid phone or password")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive")
        return cleaned_data


class MemberCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm password"
    )

    image_file = forms.ImageField(required=False, label="Profile Image")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "date_of_birth",
            "gender",
            "language",
            "color",
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
