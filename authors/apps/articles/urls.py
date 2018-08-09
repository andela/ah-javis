from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LikesAPIView, DislikesAPIView, RateAPIView,
    ArticleAPIView, CommentsListCreateAPIView, CommentsCreateDestroyAPIView
)

app_name = "articles"
router = DefaultRouter()
router.register('articles', ArticleAPIView, base_name='articles')

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<article_slug>/comments/', 
        CommentsListCreateAPIView.as_view() , name="comments"),
    path('articles/<article_slug>/comments/<comment_pk>/', 
        CommentsCreateDestroyAPIView.as_view() , name="comment"),
    path('articles/<slug>/like/', LikesAPIView.as_view(), name="like"),
    path('articles/<slug>/dislike/', DislikesAPIView.as_view(), name="dislike"),
    path('articles/<slug>/rate/', RateAPIView.as_view(), name="rate")
]
