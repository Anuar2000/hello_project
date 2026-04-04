from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UsersViewSet, PostsViewSet, CommentsViewSet, 
    MediaViewSet, LikesViewSet, FollowsViewSet, 
    RefreshTokensViewSet, RegisterView, LoginView
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
    # Приоритетные пути
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Все вьюсеты
    path('', include(router.urls)),
]