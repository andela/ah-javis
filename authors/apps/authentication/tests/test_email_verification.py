""" This is a test file for the login feature. """
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User
from .utils import TEST_USER


class TestLogin(APITestCase):
    """ Tests the view function for login. """

    def register_user(self, user):
        """ Register User. """
        self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

    def test_send_email(self):
        """ Tests that a verification email is sent on signup """
        self.register_user(TEST_USER)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Verify your account')
