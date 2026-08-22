from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from labels.forms import LabelForm
from labels.models import Label


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request, "No tienes autorización. Por favor, inicia sesión."
        )
        return redirect("login")


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/labels_list.html"
    context_object_name = "labels"


class LabelCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels_list")
    success_message = "Etiqueta creada con éxito"


class LabelUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels_list")
    success_message = "Etiqueta actualizada con éxito"


class LabelDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels_list")
    success_message = "Etiqueta eliminada con éxito"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(
                request,
                "No es posible eliminar la etiqueta porque está en uso",
            )
            return redirect("labels_list")
        return super().post(request, *args, **kwargs)
