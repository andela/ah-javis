import json
import jwt
from authors.apps.authentication.models import User
from django.test import TestCase
from authors.apps.core.email import SendMail
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from authors.apps.authentication.serializers import RegistrationSerializer
from authors.apps.authentication.utils import generate_token
from rest_framework.test import (APIClient, APIRequestFactory,
                                 force_authenticate)


class ViewTestCase(TestCase):
    """ Test case for the api views. """

    def setUp(self):
        # self.serializer_class = RegistrationSerializer()
        # user = request.data.get('user', {})
        self.testUser1 = {
            "user": {
                "username": "Tester",
                "email": "denniswanjiru71@gmail.com",
                "password": "Pass@1234",
                "pk": 34
            }
        }
        self.serializer = RegistrationSerializer(
            data=self.testUser1)
        self.testUser2 = {
            "user": {
                "username": "random",
                "email": "random@random.com",
                "password": "Secret@254"
            }
        }
        self.testArticle = {
            "article": {
                "title": "Testing",
                "description": "This is just a title",
                "body": "guess what?",
            }
        }
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def register_user(self, user):
        """ Register User. """
        response = self.client.post(
            reverse("authentication:registration"),
            user,
            format='json')
        response.render()
        user = json.loads(response.content)
        return user

    def login_user(self, user):
        """ Login user. """
        response = self.client.post(
            reverse("authentication:login"),
            user,
            format='json')
        response.render()
        user = json.loads(response.content)
        return user

    def test_like(self):
        self.register_user(self.testUser1)
        login = self.login_user(self.testUser1)

        token = login['user']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        response = self.client.put(
            reverse("articles:like"),
            slug="test-96xuq0xfbe",
            format="json")

        # print(response)
        # profile = json.loads(response.content)
        # details = profile["user"]
        self.assertEqual(len(mail.outbox), 1)
