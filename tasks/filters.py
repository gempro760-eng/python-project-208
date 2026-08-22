import django_filters
from django import forms
from django.contrib.auth.models import User

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Estado",
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Ejecutor",
    )
    label = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label="Etiqueta",
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
        label="Solo mis tareas",
    )

    class Meta:
        model = Task
        fields = ("status", "executor", "label", "self_tasks")

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
