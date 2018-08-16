from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from notifications.models import Notification
from rest_framework.permissions import AllowAny, IsAuthenticated
from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.profiles.renderers import ProfileJSONRenderer

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

class NotificationToggleViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = (ProfileSerializer,)
    renderers = (ProfileJSONRenderer, )

    def update(self, request):
        if request.user.get_notifications:
            request.user.get_notifications = False
        else:
            request.user.get_notifications = True
        request.user.save()
        serializer = self.serializer_class(request.user.profile, partial=True)

        return Response(serializer.data, status=status.HTTP_200_OK)