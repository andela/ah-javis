""" Module to test all the views in authentication. """
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

access_token = 'EAAEDF3WX5qQBAMymQATePIj1KGlXBTTS6909VgAMYApZBgfQFQhFDPne5s7CmWxw7fEZCrfr2j0D6bLWxWgWH1R5v8ndPDjYUd9zdPxctu7fjGDjUWHOqZBn6XYZBEZALCjVoGl7aaUiyriqr2n61sAtZA7qSeSU4EkAKidqUtsB8qoKk8ZCjrr0OTe2wyZBioyrXZBvODyL6d5BxNi8Q7dCrqUYYlNWPAuhZBPsCY3vDkDL6wrASurS0P'


class SocialViewTest(APITestCase):
    """ SocialViewTest tests the view functinality for social authentication. """

    def test_provider_required(self):
        """ Test that provider is required """

        token = {
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
        token = {
            "access_token": "",
            "provider": "facebook"
        }
        response = self.client.post(
            reverse("authentication:social"),
            token,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
