from django import forms
from django.contrib.auth.models import User

from tasks.models import Task


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Ejecutor",
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].label_from_instance = (
            lambda user: user.get_full_name() or user.username
        )
