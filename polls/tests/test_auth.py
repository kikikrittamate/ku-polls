from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class BasicAuthTests(TestCase):
    """Basic authentication"""

    def setUp(self):
        super().setUp()
        self.username = "pete"
        self.password = "123456789"
        self.user1 = User.objects.create_user(
                         username=self.username,
                         password=self.password,
                         email="vanguard.peach@gmail.com")
        self.user1.save()

    def test_user_log_in(self):
        response = self.client.post(reverse('login'), self.user)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('polls:index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_log_out(self):
        self.client.post(reverse('login'), self.user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)