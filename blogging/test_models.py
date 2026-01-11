from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment


class TestBlogModels(TestCase):
    """ Test suite for Blog Models """

    def setUp(self):
        # Set up test data
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Create a post with 'placeholder' image to test fallback logic
        self.post = Post.objects.create(
            title="Traws Eryri Trip",
            slug="traws-eryri-trip",
            author=self.user,
            location="TE",
            weather=0,  # Sunny
            content="Testing the Welsh mountains",
            status=1  # Published
        )

    def test_post_string_method_returns_title(self):
        """Test the __str__ method returns the title"""
        self.assertEqual(
            str(self.post),
            "Traws Eryri Trip",
        )

    def test_weather_icon_logic(self):
        """Test weather_icon_class returns the correct FontAwesome string"""
        self.assertEqual(
            self.post.weather_icon_class,
            "fas fa-solid fa-sun",
        )

    def test_image_fallback_logic(self):
        """
        Verify that if image is 'placeholder',
        the model returns the specific TE Cloudinary URL
        """
        expected_url = (
            "https://res.cloudinary.com/dxbvkulz4/image/upload/"
            "v1766450331/TE_dxmhjq.jpg"
        )
        self.assertEqual(self.post.get_image_url, expected_url)

    def test_like_count_increment(self):
        """Test that the number_of_likes method counts correctly"""
        self.assertEqual(
            self.post.number_of_likes(),
            0,
        )
        self.post.likes.add(self.user)
        self.assertEqual(
            self.post.number_of_likes(),
            1,
        )

    def test_comment_approved_default_is_false(self):
        """Verify that comments are not approved by default"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Great route!"
        )
        self.assertFalse(comment.approved)
