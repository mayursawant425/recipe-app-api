from rest_framework import viewsets, mixins
from rest_framework import authentication, permissions

from core import models
from recipe import serializers

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manages tags in database"""

    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_querysrt(self):
        """Returns objects of current authenticated user only"""

        return self.queryset.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        """Creates a new tag for authenticated user"""

        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Manages ingredients in database"""

    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Returns objects of current authenticated users only"""

        return self.queryset.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        """Creates a new ingredient object for authenticated user"""

        serializer.save(user=self.request.user)
