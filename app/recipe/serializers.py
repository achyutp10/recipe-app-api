"""Serializers for recipe API"""

from rest_framework import serializers
from core.models import Recipe
from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
  """Serializers for tags"""

  class Meta:
    model = Tag
    fields = ['id', 'name']
    read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
  """Serializer for recipe"""

  tags = TagSerializer(many=True, required=False)

  class Meta:
    model = Recipe
    fields = ['id','title','time_minutes','price','link','tags']
    read_only_field = ['id']

  def _get_or_create_tags(self, tags, recipe):
    """Handle getting or creating tags as needed"""
    auth_user = self.context['request'].user
    for tag in tags:
      tag_obj, created = Tag.objects.get_or_create(
        user=auth_user,
        **tag,
      )
      recipe.tags.add(tag_obj)
  
  def create(self, validated_data):
    """Create a recipe"""
    tags = validated_data.pop('tags', [])
    recipe = Recipe.objects.create(**validated_data)
    self._get_or_create_tags(tags, recipe)
    
    return recipe
  
  def update(self, instance, validated_data):
    """Update recipe"""
    tags = validated_data.pop('tags', None)
    if tags is not None:
      instance.tags.clear()
      self._get_or_create_tags(tags, instance)
    
    for attr, value in validated_data.items():
      setattr(instance,attr,value)

    instance.save()
    return instance

class RecipeDetailSerializer(RecipeSerializer):
  """Serializer for ecipe detail view"""
  class Meta(RecipeSerializer.Meta):
    fields = RecipeSerializer.Meta.fields + ['description']

