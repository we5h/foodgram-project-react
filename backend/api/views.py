from core.pagination import CustomPagination
from rest_framework import status, viewsets, views
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from .serializers import UserSerializer, PasswordSerializer, FollowSerializer, FollowToSerializer
from users.models import Follow
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
