from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class LabelCRUDTestCase(TestCase):
    fixtures = ("users.json", "statuses.json", "labels.json")

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password("password123")
        self.user.save()

        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)

    def test_label_list_unauthenticated(self):
        response = self.client.get(reverse("labels_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_label_list_authenticated(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("labels_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label1.name)
        self.assertContains(response, self.label2.name)

    def test_label_creation(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("label_create"),
            {"name": "Documentación"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))
        self.assertTrue(Label.objects.filter(name="Documentación").exists())

    def test_label_update(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("label_update", kwargs={"pk": self.label1.pk}),
            {"name": "Bug Crítico"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, "Bug Crítico")

    def test_label_delete_unused(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("label_delete", kwargs={"pk": self.label2.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))
        self.assertFalse(Label.objects.filter(pk=self.label2.pk).exists())

    def test_label_delete_used_in_task_forbidden(self):
        status = Status.objects.get(pk=1)
        task = Task.objects.create(
            name="Tarea con etiqueta",
            status=status,
            author=self.user,
        )
        task.labels.add(self.label1)

        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("label_delete", kwargs={"pk": self.label1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))
        self.assertTrue(Label.objects.filter(pk=self.label1.pk).exists())
