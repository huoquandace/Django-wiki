from django.test import TestCase
from http import HTTPStatus

from ts.models import *


class PostModelTest(TestCase):
    
    def test_post_model_exists(self):
        posts = Post.objects.count()
        self.assertEqual(posts, 0)
    
    def test_string_rep_of_objects(self):
        post = Post.objects.create(
            title = 'Test Post',
            body = 'Test Body'
        )
        self.assertEqual(str(post), post.title)


class HomepageTest(TestCase):
    def setUp(self):
        post1 = Post.objects.create(
            title = 'Sample post 1',
            body = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae ex rhoncus, vulputate neque non, elementum augue. Morbi pharetra lectus a odio molestie rhoncus. Proin volutpat turpis dapibus, cursus lectus sagittis, scelerisque lectus. Phasellus hendrerit quam sit amet tellus posuere, quis placerat neque facilisis. Etiam eu sollicitudin orci, a mollis lacus. Fusce lobortis metus leo, at dapibus orci facilisis quis. Etiam semper dolor turpis, eu lobortis ante cursus nec. In molestie ullamcorper accumsan.'
        )
        post2 = Post.objects.create(
            title = 'Sample post 2',
            body = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae ex rhoncus, vulputate neque non, elementum augue. Morbi pharetra lectus a odio molestie rhoncus. Proin volutpat turpis dapibus, cursus lectus sagittis, scelerisque lectus. Phasellus hendrerit quam sit amet tellus posuere, quis placerat neque facilisis. Etiam eu sollicitudin orci, a mollis lacus. Fusce lobortis metus leo, at dapibus orci facilisis quis. Etiam semper dolor turpis, eu lobortis ante cursus nec. In molestie ullamcorper accumsan.'
        )
    def test_homepage_returns_correct_response(self):
        response = self.client.get('/ts/')

        self.assertTemplateUsed(response, 'posts/index.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_returns_post_list(self):
        response = self.client.get('/ts/')

        self.assertContains(response, 'Sample post 1')
        self.assertContains(response, 'Sample post 2')