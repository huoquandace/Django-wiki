from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Hello World")