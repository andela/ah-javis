import sys
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend
from requests.exceptions import HTTPError
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, SocialSerializer
)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class SocialSignUp(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SocialSerializer

    def create(self, request,  *args, **kwargs):
        # Get access token and create user or authenticate

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        authed_user = request.user if not request.user.is_anonymous else None
        provider = serializer.data['provider']

        strategy = load_strategy(request)
        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend as e:
            return Response({
                "errors": {
                    "provider":["Provider not found.", str(e)]
                }

                },status=status.HTTP_404_NOT_FOUND)
        if isinstance(backend, BaseOAuth2):
            # Grab the access_token
            token = serializer.data['access_token']

        try:
            # if authed_user is None, make a new user,
            # else this social account will be associated with the user you pass in
            user = backend.do_auth(token, user=authed_user)
        except BaseException as e:
            # You can't associate a social account with more than user for some reason

            return Response({"errors": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        if user and user.is_active:
            serializer = UserSerializer(user)

            # if the access token was set to an empty string, then save the access token
            # from the request
            auth_created = user.social_auth.get(provider=provider)
            if not auth_created.extra_data['access_token']:
                auth_created.extra_data['access_token'] = token
                auth_created.save()

            # Set instance to user
            serializer.instance = user

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": "Error with social authentication"},
                            status=status.HTTP_400_BAD_REQUEST)
