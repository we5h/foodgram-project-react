from core.pagination import CustomPagination
from rest_framework import status, viewsets, views, filters
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from .serializers import (UserSerializer, PasswordSerializer,
                          FollowSerializer, FollowToSerializer,
                          TagSerializer, IngredientSerializer,
                          RecipeSerializer, RecipePartSerializer,
                          RecipeAddSerializer)
from users.models import Follow
from core.filters import RecipeFilter
from food.models import Tag, Ingredient, Recipe, Favorite, Cart
from . permissions import AdminOrReadOnly, IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Кастомный Вьюсет для User.
    Реализован отлично от библиотеки djoser
    для установки пагинации.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(methods=["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"status": "password set"})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class FollowViewSet(ListAPIView):
    """Подписки пользователя"""
    serializer_class = FollowSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()


class FollowToView(views.APIView):
    """Подписка/отписка пользователя"""
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        data = {'author': author.id, 'user': user.id}
        serializer = FollowToSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        following = get_object_or_404(
            Follow, user=user, author=author
        )
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Теги.
    Изменение и создание тэгов разрешено только админам.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Ингридиенты.
    Поиск по вхождению в название.
    """

    class CustomSearchFilter(filters.SearchFilter):
        search_param = "name"

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ('^name', )


class RecipeViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeAddSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request, pk)
        else:
            return self.delete_recipe(Favorite, request, pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(Cart, request, pk)
        else:
            return self.delete_recipe(Cart, request, pk)

    # @action(
    #     detail=False,
    #     permission_classes=(IsAuthenticated,)
    # )
    # def download_shopping_cart(self, request):

    def add_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if model.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError('Already added.')
        model.objects.create(recipe=recipe, user=user)
        serializer = RecipePartSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        obj = get_object_or_404(model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
