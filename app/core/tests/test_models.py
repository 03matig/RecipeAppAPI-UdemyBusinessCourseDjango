

"""
Tests for models.
Any test that apply to models inside our core app
"""

from django.test import TestCase  # Base class for our tests
from django.contrib.auth import get_user_model  # Helper function provided to django in order to get the default user model for the project


class ModelTests(TestCase):
    """ Test models. """

    def test_creat_user_with_email_successful(self):
        """ Test creating a user with an email is successful. """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))  # Checks if the password is correct; check_password is a native Django method. password needs to be a hashed password.

    def test_new_user_email_normalized(self):
        """ Test to normalize user email addresses for new users. """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],  # First element is going to be the email address and the second one is the expected email address
            ['Test2@Example.com', 'Test2@example.com'],  # First character of the email address is still unique. After the @ simbol, we need to not have any capitalization ever.
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123') # Password doesn't matter, we're not testing the password functionality.
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Tests that creationg a user without an email raises a ValueError """
        with self.assertRaises(ValueError):  # We make sure we expect the error raising.
            get_user_model().objects.create_user(None, 'sample123')

    def test_create_superuser(self):
        """ Test creating a superuser. """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)  # Field provided by PermissionsMixin
        self.assertTrue(user.is_staff)  # Allows to have access to everything inside Django Admin