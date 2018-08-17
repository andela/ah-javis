from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from notifications.models import Notification
from rest_framework.permissions import AllowAny, IsAuthenticated
from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.profiles.renderers import ProfileJSONRenderer

from authors.apps.ah_notifications.serializers import NotificationSerializer
from authors.apps.ah_notifications.renderers import NotificationJSONRenderer



class NotificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer
    renderer_classes = (NotificationJSONRenderer,)

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user)

        serializer = self.serializer_class(
            notifications, many=True, context={'request': request})

        return Response(serializer.data)
