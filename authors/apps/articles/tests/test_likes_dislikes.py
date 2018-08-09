import json
import jwt
from authors.apps.authentication.models import User
from django.test import TestCase
from authors.apps.core.email import SendMail
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from authors.apps.articles.models import Article
from authors.apps.authentication.serializers import RegistrationSerializer
from authors.apps.authentication.utils import generate_token
from rest_framework.test import (APIClient, APIRequestFactory,
                                 force_authenticate)


class ViewTestCase(TestCase):
    """ Test case for the api views. """

    def setUp(self):
        self.title = 'My awesome title'
        self.body = 'this is a test body'
        self.description = 'testing'

        self.testUser1 = {
            "user": {
                "username": "Tester",
                "email": "fry@futur.ama",
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

    def create_a_user(
            self, username='Tester', email='fry@futur.ama',
            password='Pass@1234'):
        """
        Create a test user
        """
        user = User.objects.create_user(username, email, password)
        user.save()
        return user

    def register_user(self, user):
        """ Login user. """
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

    def create_article(self):
        """
        Create a test article
        """
        user = self.create_a_user()
        article = Article.objects.create(
            title=self.title,
            description=self.description,
            body=self.body, author=user.profile)
        article.save()
        return article

    def like_article(self, token, slug):
        """
        Likes an article
        """
        res = self.client.put(
            '/api/articles/'+slug+'/like/',
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )

        return json.loads(res.content)

    def dislike_article(self, token, slug):
        """
        Likes an article
        """
        res = self.client.put(
            '/api/articles/'+slug+'/dislike/',
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )

        return json.loads(res.content)

    def test_like(self):
        article = self.create_article()
        user = self.login_user(self.testUser1)
        token = user['user']['token']
        response = self.like_article(token, article.slug)
        self.assertEqual(response['article']['likes_count'], 1)

    def test_like_a_disliked_article(self):
        article = self.create_article()
        user = self.login_user(self.testUser1)
        token = user['user']['token']
        response = self.dislike_article(token, article.slug)
        response = self.like_article(token, article.slug)
        self.assertEqual(response['article']['likes_count'], 1)

    def test_like_404_article(self):
        self.register_user(self.testUser2)
        user = self.login_user(self.testUser2)
        token = user['user']['token']
        response = self.like_article(token, 'fake-slug-h23ener32')
        self.assertEqual(response['article']['detail'],
                         'An article with this slug does not exist')

    def test_dislike(self):
        article = self.create_article()
        self.register_user(self.testUser1)
        user = self.login_user(self.testUser1)
        token = user['user']['token']
        response = self.dislike_article(token, article.slug)
        self.assertEqual(response['article']['dislikes_count'], 1)

    def test_dislike_a_liked_article(self):
        article = self.create_article()
        self.register_user(self.testUser1)
        user = self.login_user(self.testUser1)
        token = user['user']['token']
        response = self.like_article(token, article.slug)
        response = self.dislike_article(token, article.slug)
        self.assertEqual(response['article']['dislikes_count'], 1)

    def test_dislike_404_article(self):
        self.create_a_user(username='random', email='random@random.com',
                           password='Secret@254')
        user = self.login_user(self.testUser2)
        token = user['user']['token']
        response = self.dislike_article(token, 'fake-slug-h23ener32')
        self.assertEqual(response['article']['detail'],
                         'An article with this slug does not exist')
