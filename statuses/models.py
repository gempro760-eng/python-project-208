from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Nombre")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    def __str__(self):
        return self.name
