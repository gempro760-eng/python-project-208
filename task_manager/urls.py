from django.contrib import admin
from django.urls import include, path

from task_manager import views
from users.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("tasks/", include("tasks.urls")),
    path("labels/", include("labels.urls")),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
