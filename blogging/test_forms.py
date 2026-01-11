from django.test import TestCase
from .forms import CommentForm


class TestCommentForm(TestCase):
    """ Test suite for the Comment Form """

    def test_form_is_valid(self):
        """ Test form with valid data """
        form = CommentForm(
            {'body': 'This is a great trail!'},
        )
        self.assertTrue(
            form.is_valid(), msg="Form should be valid with content"
        )

    def test_form_is_invalid_empty(self):
        """ Test form with empty data """
        form = CommentForm({'body': ''})
        self.assertFalse(
            form.is_valid(), msg="Form should be invalid when empty"
        )

    def test_form_has_only_body_field(self):
        """ Verify only the 'body' field is rendered in the form """
        form = CommentForm()
        self.assertEqual(len(form.fields), 1)
        self.assertIn('body', form.fields)
