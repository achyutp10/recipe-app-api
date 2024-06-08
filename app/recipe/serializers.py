"""Serializers for recipe API"""

from rest_framework import serializers
from core.models import Recipe
from core.models import Tag

class RecipeSerializer(serializers.ModelSerializer):
  """Serializer for recipe"""

  class Meta:
    model = Recipe
    fields = ['id','title','time_minutes','price','link']
    read_only_field = ['id']

class RecipeDetailSerializer(RecipeSerializer):
  """Serializer for ecipe detail view"""
  class Meta(RecipeSerializer.Meta):
    fields = RecipeSerializer.Meta.fields + ['description']

class TagSerializer(serializers.ModelSerializer):
  """Serializers for tags"""

  class Meta:
    model = Tag
    fields = ['id', 'name']
    read_only_fields = ['id']