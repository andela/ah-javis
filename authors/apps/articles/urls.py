from django.urls import path

from .views import (
    LikesAPIView, DislikesAPIView
)

app_name = "artiles"

urlpatterns = [
    path('articles/<slug>/like/', LikesAPIView.as_view(), name="like"),
    path('articles/<slug>/dislike/', DislikesAPIView.as_view(), name="dislike")
]
