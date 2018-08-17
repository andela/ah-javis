from django.urls import path

from authors.apps.ah_notifications.views import NotificationAPIView

app_name = "ah_notifications"

urlpatterns = [
    path('notifications/', NotificationAPIView.as_view(), name="ah_notifications")
]
