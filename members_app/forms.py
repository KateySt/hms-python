from django.forms import ModelForm, TextInput, ColorInput, SelectMultiple

from members_app.models import Member


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['phone', 'color', 'courses']
        widgets = {
            'phone': TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'color': ColorInput(),
            'courses': SelectMultiple(attrs={'size': 5}),
        }
