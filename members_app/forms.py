from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.forms import (
    ModelForm,
    TextInput,
    ColorInput,
    SelectMultiple,
    CheckboxSelectMultiple,
    Select,
    DateInput
)

User = get_user_model()


class MemberForm(ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=CheckboxSelectMultiple(),
        required=False,
        label="Permissions"
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance", None)

        super().__init__(*args, **kwargs)

        permissions = Permission.objects.all().order_by(
            'content_type__app_label',
            'codename'
        )

        self.fields['user_permissions'].choices = [
            (perm.id, f"{perm.content_type.app_label}.{perm.codename} — {perm.name}")
            for perm in permissions
        ]

        if instance:
            self.fields['user_permissions'].initial = (
                instance.user_permissions.values_list("id", flat=True)
            )

    class Meta:
        model = User
        fields = [
            'phone',
            'color',
            'courses',
            'user_permissions',
            'gender',
            'language',
            'date_of_birth'
        ]
        widgets = {
            'phone': TextInput(attrs={'placeholder': 'Enter phone'}),
            'color': ColorInput(),
            'courses': SelectMultiple(attrs={'size': 5}),
            'gender': Select(),
            'language': Select(),
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }
