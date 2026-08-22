from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_task_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="name",
            field=models.CharField(
                error_messages={"unique": "Una tarea con este nombre ya existe."},
                max_length=150,
                unique=True,
                verbose_name="Nombre",
            ),
        ),
    ]