from rest_framework import serializers

from core import models


class TagSerializer(serializers.ModelSerializer):
    """Serializes tag object"""

    class Meta:
        model = models.Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializes ingredient object"""

    class Meta:
        model = models.Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializes recipe object"""

    ingredients = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = models.Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = models.Tag.objects.all()
    )

    class Meta:
        model = models.Recipe
        fields = [
            'id', 'title', 'ingredients', 'tags', 'price', 'time_minutes',
            'link',
        ]
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer recipe object with details of ingredients and tags"""

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading recipe image"""

    class Meta:
        model = models.Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
