import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.test import override_settings
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article

from authors.apps.ah_notifications.views import NotificationAPIView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authors.apps.authentication.utils import generate_token
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

class NotificationTestCase(APITestCase):
    def setUp(self):
        """ Initialize default data. """
        self.client = APIClient()
        self.user = self.create_a_user()
        self.client.force_authenticate(user=self.user)

    def create_a_user(self, username='test', email='info@test.co',
                      password='Test123.'):
        """
        Create a test user
        """
        user = User.objects.create_user(username, email, password)
        user.save()
        return user

    def test_get_notification_when_follwing_creates_article(self):
        self.client.put(reverse("authentication:user"), {
            "user":{
                "get_notifications":True}
            }, format='json')
        new_user = self.create_a_user(username='test2', email='info@test2.co',
                      password='Test123.')
        
        self.user.profile.follow(new_user.profile)
        article = Article(body="Hello aticle,", author=new_user.profile,title="A test")
        article.save()

        response = self.client.get(reverse("ah_notifications:ah_notifications"))
        self.assertEqual(len(json.loads(response.content)['notifications']), 1)

    
    def test_subscribe(self):
        response = self.client.put(reverse("authentication:user"), {
            "user":{
                "get_notifications":True}
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            json.loads(response.content).get('user').get('get_notifications')
        )
        
        response = self.client.put(reverse("authentication:user"), {
            "user":{
                "get_notifications":False}
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            json.loads(response.content).get('user').get('get_notifications')
        )
