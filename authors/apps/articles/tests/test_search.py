import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.urls import reverse
from authors.apps.articles.models import Article

from .test_models import CreateArticle
from authors.apps.articles.models import Article


class TestSearch(APITestCase):
    """
    Test user search for articles from title, description, body, author
    """
    client = APIClient()

    def test_user_search_from_article_title(self):
        article = CreateArticle().create_article()

        url = reverse("articles:filter_search") + '?search=my'
        response = self.client.get(url)
        response.render()
        results = json.loads(response.content)
        title = results[0]['title']
        self.assertEquals(title, 'My awesome title')
        self.assertIsInstance(results, list)

    def test_user_search_from_non_existent_article_title(self):
        url = reverse("articles:filter_search") + '?search=how'
        response = self.client.get(url)
        response.render()
        results = json.loads(response.content)
        self.assertEquals(results, [])
        self.assertIsInstance(results, list)

    def test_user_search_from_article_body(self):
        article = CreateArticle().create_article()

        url = reverse("articles:filter_search") + '?search=this'
        response = self.client.get(url)
        response.render()
        results = json.loads(response.content)
        body = results[0]['body']
        self.assertEquals(body, 'this is a test body')
        self.assertIsInstance(results, list)

    def test_user_search_from_non_existent_article_body(self):
        url = reverse("articles:filter_search") + '?search=how'
        response = self.client.get(url)
        response.render()
        results = json.loads(response.content)
        self.assertEquals(results, [])
        self.assertIsInstance(results, list)

    def test_user_search_from_article_description(self):
        article = CreateArticle().create_article()

        url = reverse("articles:filter_search") + '?search=this'
        response = self.client.get(url)
        response.render()
        results = json.loads(response.content)
        description = results[0]['description']
        self.assertEquals(description, 'testing')
        self.assertIsInstance(results, list)

    def test_user_search_from_non_existent_article_description(self):
        url = reverse("articles:filter_search") + '?search=how'
        response = self.client.get(url)
        response.render()
        results = json.loads(response.content)
        self.assertEquals(results, [])
        self.assertIsInstance(results, list)

    def test_user_search_from_article_author(self):
        article = CreateArticle().create_article()

        url = reverse("articles:filter_search") + '?search=this'
        response = self.client.get(url)
        response.render()
        results = json.loads(response.content)
        author = results[0]['author']['username']
        self.assertEquals(author, 'fry')
        self.assertIsInstance(results, list)

    def test_user_search_from_non_existent_article_author(self):
        url = reverse("articles:filter_search") + '?search=how'
        response = self.client.get(url)
        response.render()
        results = json.loads(response.content)
        self.assertEquals(results, [])
        self.assertIsInstance(results, list)
