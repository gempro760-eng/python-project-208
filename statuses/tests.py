from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task


class StatusCRUDTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="status_user",
			password="password123",
		)
		self.status = Status.objects.create(name="Nuevo")

	def test_status_list_requires_authentication(self):
		response = self.client.get(reverse("statuses_list"))
		self.assertRedirects(response, reverse("login"))

	def test_status_crud(self):
		self.client.login(username="status_user", password="password123")
		create_response = self.client.post(
			reverse("status_create"),
			{"name": "En progreso"},
		)
		self.assertRedirects(create_response, reverse("statuses_list"))
		created_status = Status.objects.get(name="En progreso")

		update_response = self.client.post(
			reverse("status_update", kwargs={"pk": created_status.pk}),
			{"name": "Finalizado"},
		)
		self.assertRedirects(update_response, reverse("statuses_list"))
		self.assertTrue(Status.objects.filter(name="Finalizado").exists())

		delete_response = self.client.post(
			reverse("status_delete", kwargs={"pk": created_status.pk}),
		)
		self.assertRedirects(delete_response, reverse("statuses_list"))
		self.assertFalse(Status.objects.filter(pk=created_status.pk).exists())

	def test_status_linked_to_task_cannot_be_deleted(self):
		Task.objects.create(
			name="Tarea protegida",
			status=self.status,
			author=self.user,
		)
		self.client.login(username="status_user", password="password123")

		response = self.client.post(
			reverse("status_delete", kwargs={"pk": self.status.pk}),
		)

		self.assertRedirects(response, reverse("statuses_list"))
		self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
