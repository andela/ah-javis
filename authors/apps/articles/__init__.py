from django.apps import AppConfig


class ArticlesAppConfig(AppConfig):
    name = 'authors.apps.articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import authors.apps.articles.signals


# This is how we register our custom app config with Django. Django is smart
# enough to look for the `default_app_config` property of each registered app
# and use the correct app config based on that value.
default_app_config = 'authors.apps.articles.ArticlesAppConfig'
