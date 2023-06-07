from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'first_name')
    list_filter = ('email', 'first_name')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
