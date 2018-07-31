""" module to test all the views in authentication. """
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User
from .utils import TEST_USER, create_user

class RegisterViewTest(APITestCase):
    """ RegisterViewTest tests the view register validations error messages. """

    def setUp(self):
        """ Create a default user. """
        create_user()        

    def test_email_is_valid(self):
        """ test that email is a valid email. """
        user = {
            "user": {
                "email": "testuser",
                "username": "testuser",
                "password": "testspassword"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')
        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['email'][0], "Enter a valid email address.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_cannot_be_register_twice(self):
        """ Test that email can not beregistered twice. """
        
        user = {
            "user": {
                "email": "test@gmail.com",
                "username": "testuser",
                "password": "testspassword"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_username_cannot_be_register_twice(self):
        """ Test that username can not beregistered twice. """
        
        user = {
            "user": {
                "email": "test@gmail.com",
                "username": "testuser",
                "password": "testspassword"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['username'][0], "user with this username already exists.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_cannot_be_lass_than_8_characters(self):
        """Test that password cannot be less than 8 characters"""

        user = {
            "user": {
                "email": "test3@gmail.com",
                "username": "testuser3",
                "password": "tests"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['error'][0], "Password should be atleats 8 characters.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_Not_being_alphanumeric(self):
        """Test that password should contain alphanumeric characters."""

        user = {
            "user": {
                "email": "test4@gmail.com",
                "username": "testuser4",
                "password": "testspass"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        error = errors
        self.assertEqual(error[0], "Password should have atleast an uppercase, number and special character.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
