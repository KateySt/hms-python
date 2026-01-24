from django import forms

from chart_app.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Enter your message...",
                    "rows": 2,
                    "class": "form-control",
                }
            )
        }

    def clean_message(self):
        msg = self.cleaned_data.get("message")
        if not msg or msg.strip() == "":
            raise forms.ValidationError("Message cannot be empty")
        return msg
