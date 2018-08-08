from django.conf.urls import url

from .views import (ProfileRetrieveAPIView, ProfileFollowAPIView)

app_name = 'profiles'

urlpatterns = [
    url(r'^(?P<username>\w+)/?$',
        ProfileRetrieveAPIView.as_view(), name="view_profile"),
    url(r'^(?P<username>\w+)/follow/?$',
        ProfileFollowAPIView.as_view(), name="follow_profile"),
]
