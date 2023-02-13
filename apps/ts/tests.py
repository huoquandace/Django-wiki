from django.test import TestCase

from ts.models import *


class PostModelTest(TestCase):
    
    def test_post_model_exists(self):
        posts = Post.objects.count()
        self.assertEqual(posts, 0)
    
    def test_string_rep_of_objects(self):
        post = Post.objects.create(
            title = "Test Post",
            body = "Test Body"
        )
        self.assertEqual(str(post), post.title)