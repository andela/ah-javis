import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User

"""Configure JWT Here"""
class JWTAuthentication:
    ''' JWTAuthentication imprements jwt authentication '''

    def authenticate(self, request):
        pass
