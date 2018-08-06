from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from authors.apps.core.utils import random_string_generator
from authors.apps.core.models import TimeModel
from django.contrib.auth.models import User

class Article(TimeModel):
    ''' Model ..... '''
    slug = models.CharField(db_index=True, max_length=255)
    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()
    body = models.TextField()

    author = models.ForeignKey(
                    'profiles.Profile',
                    on_delete=models.CASCADE,
                    related_name='articles')
    # default image for the article.
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Article)
def add_slug_to_article_if_not_exists(sender, instance, *args, **kwargs):
    """ create a signal to add slug field if None exists. """
    MAXIMUM_SLUG_LENGTH = 255

    if instance and not instance.slug:
        slug = slugify(instance.title)
        unique = random_string_generator()

        if len(slug) > MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH]

        while len(slug + '-' + unique) > MAXIMUM_SLUG_LENGTH:
            parts = slug.split('-')

            if len(parts) is 1:
                slug = slug[:MAXIMUM_SLUG_LENGTH - len(unique) - 1]
            else:
                slug = '-'.join(parts[:-1])

        instance.slug = slug + '-' + unique

class Rate(models.Model):
    """Ratings model."""
    rates = models.IntegerField()
    counter = models.IntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rater = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

@receiver(pre_save, sender=Rate)
def add_one_to_counter(sender, instance, *args, **kwargs):
    """ create a signal to add counter value by one. """

    instance.counter = instance.counter + 1
