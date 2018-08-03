""" Module to test all the views in authentication. """
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

access_token = 'EAAEDF3WX5qQBAKhSWoHbqX3RIENvLSUCWeNKWT4nl3owVdj0QHlpqMMT0t4aRZCKA4P6aLTPJwv1afcDooJxZCR0GCPNmqSRzEwQ9sJkuh1cGl7e7TBghQaF2JM3krY5owyOSMg5dvMluslSZBQR2j4itOhDJ4tzrmZAs9DhiKyuIpZBZCHt1fJXlaapz1GDPnIHVUO5bxGsbF5gvVmq2SsJkc0SomZBAhe75VZCHsZCf8uRyomk2LZCd3'
class SocialViewTest(APITestCase):
    """ SocialViewTest tests the view functinality for social authentication. """

    def test_provider_required(self):
        """ Test that provider is required """

        token =  {
                "access_token": access_token,
                "provider": ""
            }
        response = self.client.post(
            reverse("authentication:social"),
            token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_token_required(self):
        """ Test that token is required """
        token =  {
                "access_token": "",
                "provider": "facebook"
            }
        response = self.client.post(
            reverse("authentication:social"),
            token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_is_returned(self):
        """ Test that user is returned """
        token =  {
                "access_token": access_token,
                "provider": "facebook"
            }
        response = self.client.post(
            reverse("authentication:social"),
            token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
