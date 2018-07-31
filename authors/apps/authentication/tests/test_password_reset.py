from django.test import TestCase
from .utils import TEST_USER
from rest_framework import status
from django.urls import reverse


class TestPasswordReset(TestCase):
    """ Tests the password reset feature. """

    EMAIL = {
        "email": "test@mail.com"
    }
    NEW_PASSWORD = {
        "password": "newpassword"
    }

    def register_user(self, user):
        """ Register User. """
        self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

    def test_user_can_receive_reset_password_email(self):
        """ Tests that a registered user can receive a reset
        password email. """
        self.register_user(TEST_USER)

        response = self.client.post(
            reverse("authentication:forgot_password"),
            self.EMAIL, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_reset_password(self):
        """ Tests if the user can reset(update) their password. """
        self.register_user(TEST_USER)

        response = self.client.post(
            reverse("authentication:forgot_password"),
            self.EMAIL, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse("authentication:reset_password"),
            self.NEW_PASSWORD, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
