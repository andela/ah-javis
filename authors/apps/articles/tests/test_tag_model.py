from django.test import TestCase

from authors.apps.articles.models import Tag

class ModelTestCase(TestCase):
    """
    This class defines the test suite for the tag model.
    """

    def test_model_can_create_a_taglist(self):
        """
        Test the tag model can create ataglist
        """

        response = Tag.objects.create(
            tag = ['django', 'Django-rest']
        )
        self.assertTrue(isinstance(response, Tag))

    def test_model_returns_readable_representation(self):
        """
        Test a readable string is returned for the model instance.
        """

        response = Tag.objects.create(
            tag = ['django-rest', 'django']
        )
        self.assertIn('django-rest', str(response))
