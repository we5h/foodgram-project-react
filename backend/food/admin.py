from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through


class TagsInLine(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'color',
        'slug'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name',
                    'measurement_unit')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'author',
                    'count_favorite')
    list_filter = ('name',
                   'author',
                   'tags')
    inlines = (IngredientsInLine, TagsInLine)

    def count_favorite(self, instance):
        return instance.favorites.count()


@admin.register(IngredientAmount)
class IngredientAmount(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user'
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user'
    )
