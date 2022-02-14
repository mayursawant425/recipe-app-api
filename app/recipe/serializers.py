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
