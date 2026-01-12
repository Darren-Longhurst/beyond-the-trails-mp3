from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class TestBlogViews(TestCase):
    def setUp(self):
        # 1. Setup Users
        self.user = User.objects.create_user(username="author", password="password")
        self.other_user = User.objects.create_user(username="hacker", password="password")

        # 2. Setup Post
        self.post = Post.objects.create(
            title="Trail", slug="trail", author=self.user, status=1, weather=1, bike_choice=1
        )

        # 3. Setup Comment
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, body="Original Comment", approved=True
        )

    ## --- TARGETING POST_DETAIL --- ##

    def test_post_detail_view_with_comment_submission(self):
        """ Test that a logged-in user can submit a comment """
        self.client.login(username="author", password="password")
        response = self.client.post(reverse('post_detail', args=['trail']), {
            'body': 'This is a new test comment'
        })
        self.assertEqual(response.status_code, 302) # Should redirect after POST
        self.assertEqual(Comment.objects.count(), 2)

    def test_unapproved_comment_visibility(self):
        """ Verify unapproved comments are only seen by the author """
        unapproved = Comment.objects.create(
            post=self.post, author=self.user, body="Hidden", approved=False
        )
        # Logged in as hacker (not author)
        self.client.login(username="hacker", password="password")
        response = self.client.get(reverse('post_detail', args=['trail']))
        # Should only see the 1 approved comment from setUp
        self.assertEqual(len(response.context['comments']), 1)

    ## --- TARGETING COMMENT_EDIT --- ##

    def test_successful_comment_edit(self):
        """ Test that author can edit their own comment """
        self.client.login(username="author", password="password")
        response = self.client.post(
            reverse('comment_edit', args=['trail', self.comment.id]),
            {'body': 'Updated Body'}
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, 'Updated Body')
        self.assertFalse(self.comment.approved) # Logic says edit sets approved to False

    def test_user_cannot_edit_others_comment(self):
        """ Verify hacker cannot edit author's comment """
        self.client.login(username="hacker", password="password")
        response = self.client.post(
            reverse('comment_edit', args=['trail', self.comment.id]),
            {'body': 'Hacked!'}
        )
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.body, 'Hacked!')
        self.assertEqual(response.status_code, 302)

    ## --- TARGETING POST_DELETE --- ##

    def test_author_can_delete_post(self):
        self.client.login(username="author", password="password")
        response = self.client.get(reverse('post_delete', args=['trail']))
        self.assertEqual(Post.objects.count(), 0)

    ## --- TARGETING POST_LIST FILTERS --- ##

    def test_post_filtering_by_bike(self):
        """ Test the bike_val filter logic in PostList """
        response = self.client.get(reverse('blog') + '?bike=1')
        self.assertEqual(len(response.context['post_list']), 1)

    ## --- TARGETING ERROR HANDLERS --- ##

    def test_handler404(self):
        response = self.client.get('/not-a-real-url/')
        self.assertEqual(response.status_code, 404)
