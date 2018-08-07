from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import RateAPIView

app_name = "articles"

urlpatterns = [
    path('articles/<slug>/rate/', RateAPIView.as_view(), name="rate"),
]
