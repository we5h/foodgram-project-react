from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    email = models.EmailField(
        'email',
        unique=True,
        max_length=254
    )
    # Эти поля были переопределены из-за требования в доке.
    # Поля должны быть 'required'.
    # Без них проходит POST запрос на создание пользователя, что неверно.
    first_name = models.CharField(('first name'), max_length=150, blank=False)
    last_name = models.CharField(('last name'), max_length=150, blank=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Подписки"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following')]

    def __str__(self):
        return f'{self.user} -> {self.author}'
