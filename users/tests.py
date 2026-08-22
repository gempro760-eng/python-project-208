from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserCRUDTestCase(TestCase):
    fixtures = ('users.json',)

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user1.set_password("password123")
        self.user1.save()

        self.user2 = User.objects.get(pk=2)
        self.user2.set_password("password456")
        self.user2.save()

    def test_user_list_view(self):
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_user_creation(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "Carlos",
                "last_name": "Gomez",
                "username": "carlos_g",
                "password1": "secretpass123",
                "password2": "secretpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="carlos_g").exists())

    def test_user_update_by_owner(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("user_update", kwargs={"pk": self.user1.pk}),
            {
                "first_name": "Johnny",
                "last_name": "Doe",
                "username": "john_doe_updated",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, "Johnny")

    def test_user_update_by_other_user_forbidden(self):
        self.client.login(username="jane_doe", password="password456")
        response = self.client.post(
            reverse("user_update", kwargs={"pk": self.user1.pk}),
            {
                "first_name": "Hacked",
                "last_name": "User",
                "username": "hacked_user",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        self.user1.refresh_from_db()
        self.assertNotEqual(self.user1.first_name, "Hacked")

    def test_user_delete_by_owner(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("user_delete", kwargs={"pk": self.user1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())
