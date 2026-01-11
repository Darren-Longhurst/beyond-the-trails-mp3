from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import (
    home_page, PostList, post_detail, comment_edit, comment_delete
)


class TestUrls(SimpleTestCase):
    """ Test suite for URL resolution """

    def test_home_url_resolves(self):
        """ Tests that the root URL resolves to home_page """
        url = reverse('home')
        self.assertEqual(resolve(url).func, home_page)

    def test_blog_url_resolves(self):
        """ Tests that the blog URL resolves to PostList class view """
        url = reverse('blog')
        self.assertEqual(resolve(url).func.view_class, PostList)

    def test_post_detail_url_resolves(self):
        """ Tests the detail URL with a slug """
        url = reverse('post_detail', args=['test-slug'])
        self.assertEqual(resolve(url).func, post_detail)

    def test_comment_edit_url_resolves(self):
        """ Tests the comment edit URL with slug and ID """
        url = reverse('comment_edit', args=['test-slug', 1])
        self.assertEqual(resolve(url).func, comment_edit)

    def test_error_404_url_resolves(self):
        """ Tests the 404 test path resolve """
        url = reverse('404-test')
        # Check if you named this in path or use the path string
        response = self.client.get('/404-test/')
        self.assertEqual(response.status_code, 200)
