from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from .models import Post
from .admin import PostAdmin


class TestAdminPanel(TestCase):
    """ Test suite for the Admin Panel logic """

    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()

        # Create a superuser and a regular staff user
        self.superuser = User.objects.create_superuser(
            username="admin", password="password", email="admin@test.com"
        )
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )

        # Create posts for both
        self.post1 = Post.objects.create(
            title="Admin Post", author=self.superuser, slug="admin-post"
        )
        self.post2 = Post.objects.create(
            title="Staff Post", author=self.staff_user, slug="staff-post"
        )

    def test_post_admin_queryset_filtering(self):
        """ Verify regular staff only see their own posts in the admin list """
        ma = PostAdmin(Post, self.site)

        # Request as superuser
        request = self.factory.get('/admin')
        request.user = self.superuser
        self.assertEqual(ma.get_queryset(request).count(), 2)

        # Request as regular staff
        request.user = self.staff_user
        self.assertEqual(ma.get_queryset(request).count(), 1)
        self.assertEqual(ma.get_queryset(request)[0].author, self.staff_user)

    def test_automatic_slug_generation(self):
        """ Verify that save_model generates a unique slug even if empty """
        ma = PostAdmin(Post, self.site)
        new_post = Post(title="Unique Trail Ride", author=self.staff_user)

        # Mocking the admin save process
        request = self.factory.get('/admin')
        request.user = self.staff_user
        ma.save_model(request, new_post, form=None, change=False)

        self.assertEqual(new_post.slug, "unique-trail-ride")
