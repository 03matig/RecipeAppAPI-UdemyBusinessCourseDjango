"""
Tests for the user API.
"""

from django.test import TestCase

from django.contrib.auth import get_user_model

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """ Create and return a new user with watever details we pass it to the parameters. """
    return get_user_model().objects.create_user(**params)

# Public - unauthenticated requests or requests that don't require authentication, such as registrate a new user.
# Private - authenticated requests or requests that do require authentication (two separate classes for this)

class PublicUserApiTests(TestCase):
    """ Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email']) # We search the users in the database that matches our payload.email value

        self.assertTrue(user.check_password(payload['password'])) # In that same user, we check if password is the same than 'password'
        self.assertNotIn('password', res.data) # asserts if password is not in the response data

    def test_user_with_email_exists_error(self):
        """ Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  # If we try and register a new user with an email of an user that already exists on a database, it's going to get denied.

    def test_password_too_short_error(self):
        """ Test an error is returned if password less than 5 chars. """
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)