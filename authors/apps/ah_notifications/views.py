from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from notifications.models import Notification
from rest_framework.permissions import AllowAny, IsAuthenticated
from authors.apps.ah_notifications.serializers import NotificationSerializer



class NotificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user)

        serializer = self.serializer_class(
            notifications, many=True, context={'request': request})

        return Response(serializer.data)
