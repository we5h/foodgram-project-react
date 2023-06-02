from django.urls import include, path
from . views import (UserViewSet, FollowViewSet,
                     FollowToView,
                     TagViewSet,
                     IngredientViewSet,
                     RecipeViewSet)
from rest_framework.routers import SimpleRouter

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingridients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/subscriptions/', FollowViewSet.as_view()),
    path('users/<int:pk>/subscribe/', FollowToView.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
