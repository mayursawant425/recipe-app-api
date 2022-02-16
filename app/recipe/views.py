from rest_framework import viewsets, mixins, status
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from core import models
from recipe import serializers

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manages tags in database"""

    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Returns objects of current authenticated user only"""

        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset

        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        print(assigned_only, queryset)
        return queryset.filter(
            user=self.request.user
        ).order_by('name').distinct()

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

        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset

        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('name').distinct()

    def perform_create(self, serializer):
        """Creates a new ingredient object for authenticated user"""

        serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """Manages recipes in database"""

    serializer_class = serializers.RecipeSerializer
    queryset = models.Recipe.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def _params_to_int(self, qs):
        """Converts string params to list of int"""

        return list(map(int, qs.split(',')))

    def get_queryset(self):
        """Returns objects of current authenticated user only"""

        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_int(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_int(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user).order_by('title')

    def get_serializer_class(self):
        """Selects appropriate serializer class"""

        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Creates a new recipe object for authenticated user"""

        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Uploads image for a recipe"""

        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializers.errors, status=status.BAD_REQUEST_400)
