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
                "password": "Pass123."
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
                "password": "Pass123."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_email_is_required(self):
        """ Test that email is required. """
        
        user = {
            "user": {
                "username": "testuser",
                "password": "Pass123."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['email'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
         
    def test_email_is_not_empty(self):
        """ Test that email is not empty. """
        
        user = {
            "user": {
                "email": "",
                "username": "testuser",
                "password": "Pass123."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['email'][0], "Email is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_cannot_be_register_twice(self):
        """ Test that username can not beregistered twice. """
        
        user = {
            "user": {
                "email": "test@gmail.com",
                "username": "testuser",
                "password": "Pass123."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['username'][0], "Username is taken.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
         
    def test_username_is_required(self):
        """ Test that username is required. """
        
        user = {
            "user": {
                "email": "testuser@gmail.com",
                "password": "Pass123."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['username'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
 
    def test_username_is_not_empty(self):
        """ Test that username is not empty. """
        
        user = {
            "user": {
                "email": "test@gmail.com",
                "username": "",
                "password": "Pass123."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['username'][0], "Username is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_cannot_be_less_than_8_characters(self):
        """Test that password cannot be less than 8 characters"""

        user = {
            "user": {
                "email": "test3@gmail.com",
                "username": "testuser3",
                "password": "Pass1."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['password'][0], "Password should be atleats 8 characters.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_not_being_alphanumeric(self):
        """Test that password should contain alphanumeric characters."""

        user = {
            "user": {
                "email": "test4@gmail.com",
                "username": "testuser4",
                "password": "Testspass."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        error = errors['password']
        self.assertEqual(error[0], "A password must contain atleast one number.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_should_have_an_uppercase(self):
        """Test that password should contain uppercase character."""

        user = {
            "user": {
                "email": "test4@gmail.com",
                "username": "testuser4",
                "password": "testspass1."
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        error = errors['password']
        self.assertEqual(error[0], "Password should have an uppercase")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_should_have_a_special_character(self):
        """Test that password should contain special character."""

        user = {
            "user": {
                "email": "test4@gmail.com",
                "username": "testuser4",
                "password": "Testspass1"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        error = errors['password']
        self.assertEqual(error[0], "Password should have a special character.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_required(self):
        """ Test that password is required. """
        
        user = {
            "user": {
                "email": "testuser@gmail.com",
                "username": "testuser"
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['password'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
 
    def test_password_is_not_empty(self):
        """ Test that password is not empty. """
        
        user = {
            "user": {
                "email": "test@gmail.com",
                "username": "testuser",
                "password": ""
            }
        }
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')

        response.render()
        errors = json.loads(response.content).get("errors")
        self.assertEqual(errors['password'][0], "Password is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

