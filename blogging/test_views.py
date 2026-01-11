from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment


class TestBlogViews(TestCase):
    """ Test suite for the blog views and filtering logic """

    def setUp(self):
        self.user = User.objects.create_user(
            username="author",
            password="password",
        )
        self.other_user = User.objects.create_user(
            username="hacker",
            password="password",
        )
        self.post = Post.objects.create(
            title="Trail",
            slug="trail",
            author=self.user,
            status=1,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Original Comment",
        )

    def test_user_cannot_delete_others_comment(self):
        """ Verify that a user cannot delete a comment they didn't write """
        self.client.login(
            username="hacker",
            password="password",
        )
        response = self.client.post(
            reverse('comment_delete', args=['trail', self.comment.id])
        )

        # Should redirect and show error message
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(id=self.comment.id).exists()
        )

    def test_post_filtering_by_weather(self):
        """ Verify the PostList filtering logic works for weather """
        Post.objects.create(
            title="Rainy Ride",
            slug="rain",
            author=self.user,
            status=1,
            weather=2,
        )  # 2 = Rainy
        response = self.client.get(
            reverse('blog') + '?weather=2',
        )

        self.assertEqual(
            len(response.context['post_list']), 1
        )
        self.assertEqual(
            response.context['post_list'][0].title,
            "Rainy Ride",
        )
