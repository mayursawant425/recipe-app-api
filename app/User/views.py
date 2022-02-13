from django.shortcuts import render
from rest_framework import generics, permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from User import serializers


class CreateUserView(generics.CreateAPIView):
    """Creates a new user"""

    serializer_class = serializers.UserSerializer


class AuthTokenView(ObtainAuthToken):
    """Creates a new auth token for user"""

    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Updates own profile"""

    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrives and returns authenticated user"""

        return self.request.user
