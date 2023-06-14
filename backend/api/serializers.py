from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from food.models import (Cart, Favorite, Ingredient, IngredientAmount, Recipe,
                         Tag)
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Пользователи [GET]"""

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj
        ).exists()


class CustomUserPostSerializer(UserCreateSerializer):
    """Пользователи [POST]"""
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')


class PasswordSerializer(serializers.Serializer):
    """Смена пароля."""

    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class RecipePartSerializer(serializers.ModelSerializer):
    """Рецепт для списка подписок."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Подписки пользователя."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(
            author=obj.author, user=request.user
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipe_limit'):
            recipe_limit = int(request.GET.get('recipe_limit'))
            queryset = Recipe.objects.filter(
                author=obj.author)[:recipe_limit]
        else:
            queryset = Recipe.objects.filter(
                author=obj.author)
        serializer = RecipePartSerializer(
            queryset, read_only=True, many=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class FollowToSerializer(serializers.ModelSerializer):
    """Подписаться/удалить подписку."""
    class Meta:
        model = Follow
        fields = (
            'user',
            'author'
        )

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(
                'Unable to follow yourself.'
            )
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Already followed.'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = FollowSerializer(
            instance,
            context=context
        )
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    """Вывод тегов."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )
        read_only_fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Ингридиенты."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )
        read_only_fields = (
            'id',
            'name',
            'measurement_unit'
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    """Добавление ингридиента в рецепт."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(),
                                            source='ingredient')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Ингридиенты с количеством."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """Рецепты."""

    author = CustomUserSerializer()
    tags = TagSerializer(
        many=True,
    )
    ingredients = IngredientAmountSerializer(
        source='ingredient_in_recipe',
        read_only=True, many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def is_exists_in(self, obj, model):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.is_exists_in(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.is_exists_in(obj, Cart)


class RecipeAddSerializer(serializers.ModelSerializer):
    """Добавление рецепта."""

    image = Base64ImageField(max_length=None, use_url=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientSerializer(many=True,
                                          source='ingredient_in_recipe')
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Recipe
        fields = [
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def bulk_create_ingredients(self, ingredients, recipe):
        bulk_list = list()
        double_ing_check = set()
        for ingredient in ingredients:
            amount1 = ingredient['amount']
            ingredient1 = ingredient['ingredient']
            if ingredient1 in double_ing_check:
                raise serializers.ValidationError({"error":
                                                   "You can not add the same"
                                                   " ingredient twice."
                                                   "Change amount."})
            else:
                double_ing_check.add(ingredient1)
            bulk_list.append(IngredientAmount(
                             recipe=recipe,
                             ingredient=ingredient1,
                             amount=amount1)
                             )
        IngredientAmount.objects.bulk_create(bulk_list)

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop("ingredient_in_recipe")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        self.bulk_create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        recipe.save()
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredient_in_recipe")
        tags = validated_data.pop("tags")
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.bulk_create_ingredients(ingredients, instance)
        instance.name = validated_data.pop("name")
        instance.text = validated_data.pop("text")
        if validated_data.get("image") is not None:
            instance.image = validated_data.pop("image")
        instance.cooking_time = validated_data.pop("cooking_time")
        instance.tags.set(tags)
        instance.save()
        return instance
