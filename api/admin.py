from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Users, Posts, Comments, Likes, Follows, Media, RefreshTokens

# Регистрируем твои кастомные таблицы
admin.site.register(Users)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Follows)
admin.site.register(Media)
admin.site.register(RefreshTokens)

# Выводим системную таблицу пользователей (Auth User)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')