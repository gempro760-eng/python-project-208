from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from users.forms import UserRegistrationForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = "Usuario registrado con éxito"


class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_denied_message = "No tienes permiso para modificar a otro usuario."

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, "Debes iniciar sesión para realizar esta acción."
            )
            return redirect("login")
        messages.error(self.request, self.permission_denied_message)
        return redirect("users_list")


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users_list")
    success_message = "Usuario actualizado con éxito"


class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_list")
    success_message = "Usuario eliminado con éxito"

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar el usuario porque tiene tareas asociadas",
            )
            return redirect("users_list")


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "users/login.html"
    success_message = "Has iniciado sesión con éxito"

    def get_success_url(self):
        return reverse_lazy("index")


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Has cerrado sesión")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("index")
