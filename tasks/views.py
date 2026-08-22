from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from tasks.forms import TaskForm
from tasks.models import Task


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request, "No tienes autorización. Por favor, inicia sesión."
        )
        return redirect("login")


class TaskListView(CustomLoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Tarea creada con éxito"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Tarea actualizada con éxito"


class TaskDeleteView(
    CustomLoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Tarea eliminada con éxito"

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Solo el autor de la tarea puede eliminarla")
        return redirect("tasks_list")
