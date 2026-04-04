from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UsersViewSet, PostsViewSet, CommentsViewSet, 
    MediaViewSet, LikesViewSet, FollowsViewSet, 
    RefreshTokensViewSet, RegisterView # Не забудь импортировать RegisterView, который мы создали
)

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'posts', PostsViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'media', MediaViewSet)
router.register(r'likes', LikesViewSet)
router.register(r'follows', FollowsViewSet)
router.register(r'refresh_tokens', RefreshTokensViewSet)

urlpatterns = [
    # Все стандартные вьюсеты (посты, лайки и т.д.)
    path('', include(router.urls)),

    # 1. РЕГИСТРАЦИЯ: тот самый путь, который создаст юзера с хешем
    path('register/', RegisterView.as_view(), name='register'),

    # 2. ЛОГИН: этот эндпоинт проверит пароль и выдаст Access/Refresh токены
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Обновление токена (на будущее)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]