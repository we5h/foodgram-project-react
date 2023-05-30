from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from users.models import Follow
from djoser.serializers import UserSerializer

User = get_user_model()


class UserSerializer(UserSerializer):
    """Сериализатор пользователи"""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\Z", max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

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

    def validate_email(self, value):
        if len(value) < 254:
            return value
        raise serializers.ValidationError("Email less then 254 symbols.")

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user == obj or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj
        ).exists()


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = "__all__"
