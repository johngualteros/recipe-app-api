from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a recipe object"""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            tag_object, created = Tag.objects.get_or_create(name=tag['name'], user=auth_user)
            recipe.tags.add(tag_object)
        for ingredient in ingredients:
            ingredient_object, created = Ingredient.objects.get_or_create(name=ingredient['name'], user=auth_user)
            recipe.ingredients.add(ingredient_object)
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe object"""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = super().update(instance, validated_data)
        recipe.tags.clear()
        recipe.ingredients.clear()
        auth_user = self.context['request'].user
        for tag in tags:
            tag_object, created = Tag.objects.get_or_create(name=tag['name'], user=auth_user)
            recipe.tags.add(tag_object)
        for ingredient in ingredients:
            ingredient_object, created = Ingredient.objects.get_or_create(name=ingredient['name'], user=auth_user)
            recipe.ingredients.add(ingredient_object)
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail objects"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description', 'image')

class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes"""

    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
        extra_kwargs = {
            'image': {'required': True}
        }


