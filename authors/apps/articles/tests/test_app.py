from django.apps import apps
from django.test import TestCase, override_settings
from authors.apps.articles.apps import ArticlesConfig

@override_settings(CELERY_ALWAYS_EAGER=True)
class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ArticlesConfig.name, 'articles')
