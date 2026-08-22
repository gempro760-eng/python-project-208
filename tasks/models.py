from django.contrib.auth.models import User
from django.db import models

from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre",
        error_messages={
            "unique": "Una tarea con este nombre ya existe.",
        },
    )
    description = models.TextField(blank=True, verbose_name="Descripción")
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name="Estado",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_tasks",
        verbose_name="Autor",
    )

    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        verbose_name="Ejecutor",
    )

    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name="tasks",
        verbose_name="Etiquetas",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    def __str__(self):
        return self.name
