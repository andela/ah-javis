from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import ArticleAPIView, FavoriteAPIView

app_name = "articles"

router = DefaultRouter()
router.register('articles', ArticleAPIView, base_name='articles')

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<slug>/favorite/',
         FavoriteAPIView.as_view(), name="favorite"),
]
