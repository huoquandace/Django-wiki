from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("list_posts")

    def authenticate(self):
        self.client.post(
            reverse("signup"),
            {
                "email": "jonathan@app.com",
                "password": "password##!123",
                "username": "jonathan",
            },
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "jonathan@app.com",
                "password": "password##!123",
            },
        )

        # print(response.data)

        token = response.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_posts(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_post_creation(self):
        self.authenticate()

        sample_data = {"title": "Sample title", "content": "Sample content"}
        response = self.client.post(reverse("list_posts"), sample_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], sample_data["title"])
