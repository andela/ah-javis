from django.urls import path 
from .views import CommentsListCreateAPIView

urlpatterns = [
    path('articles/<article_slug>/comments/', 
        CommentsListCreateAPIView.as_view() , name="comments"),
]