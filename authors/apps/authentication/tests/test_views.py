""" Module to test all the views in authentication. """
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User

TEST_USER = {
    "user": {
        "email": "test@mail.com",
        "password": "testpassword",
        "username": "testuser"
    }
}


class RegisterViewTest(APITestCase):
    """ RegisterViewTest tests the view functinality for register. """

    def test_user_can_register(self):
        """ Test that we create a user object on registration. """
        # post TEST_USER to registration endpoint.
        response = self.client.post(
            reverse("authentication:registration"),
            TEST_USER,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Ensure user exist.
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, TEST_USER['user']['email'])

    def test_get_user_registration(self):
        """ Test that response contains user.  """
        response = self.client.post(
            reverse("authentication:registration"),
            TEST_USER,
            format='json')
        response.render()
        user = json.loads(response.content)
        # Test that user is a subset of TEST_USER - contains users
        self.assertTrue(set(user['user'].items()).issubset(
            set(TEST_USER['user'].items())))

    def test_email_required(self):
        """ Test that email is required on register. """
        user = {
            "user": {
                "username": "testuser",
                "password": "testspassword"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_required(self):
        """ Test that password is required on register. """
        user = {
            "user": {
                "username": "testuser",
                "email": "tests@mail.com"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_required(self):
        """ Test that username is required on register. """
        user = {
            "user": {
                "email": "test@mail.com",
                "password": "testpassword"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_twice(self):
        """ Test that user can't register twice. """
        response = self.client.post(
            reverse("authentication:registration"),
            TEST_USER,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            reverse("authentication:registration"),
            TEST_USER,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





class TestLogin(APITestCase):
    """ Tests the view function for login. """

    def register_user(self, user):
        """ Register User. """
        self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

    def test_user_can_login(self):
        """ Tests that a registered user can login. """
        self.register_user(TEST_USER)
        response = self.client.post(
            reverse("authentication:login"), TEST_USER, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure user exist.
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, TEST_USER['user']['email'])

    def test_user_logging_in_exists(self):
        """ Tests that a non-existing user cannot login. """
        response = self.client.post(
            reverse("authentication:login"), TEST_USER, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_password_required(self):
        """ Tests that email and password are both required for login. """
        response = self.client.post(
            reverse("authentication:login"), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_required(self):
        """ Tests that email is required for login. """
        user = {
            "user": {
                "password": "testpassword"
            }
        }
        response = self.client.post(
            reverse("authentication:login"), user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_required(self):
        """ Tests that password is required for login. """
        user = {
            "user": {
                "password": "",
                "email": "testemail@mail.com"
            }
        }
        response = self.client.post(
            reverse("authentication:login"), user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_is_active(self):
        """ Tests that the user logging in us not a banned user. """
        self.register_user(TEST_USER)
        user = User.objects.get()
        user.is_active = False
        user.save()
        response = self.client.post(
            reverse("authentication:login"), TEST_USER, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
