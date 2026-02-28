from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, PostsViewSet, CommentsViewSet, MediaViewSet, LikesViewSet, FollowsViewSet, RefreshTokensViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'posts', PostsViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'media', MediaViewSet)
router.register(r'likes', LikesViewSet)
router.register(r'follows', FollowsViewSet)
router.register(r'refresh_tokens', RefreshTokensViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
