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
