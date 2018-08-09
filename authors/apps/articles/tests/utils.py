from authors.apps.authentication.models import User
from authors.apps.articles.models import Article


def create_user():
    user = User(username="username", email="username@mail.com", password="Qwerty123")
    user.save()
    return user

def create_article():
    """
    Create a test article
    """
    user = User.objects.get()
    article = Article.objects.create(
                title="django",
                description="django sucks",
                body="body", author=user.profile)
    article.save()
    return article
