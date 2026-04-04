from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# ИМПОРТ МОДЕЛЕЙ
# SystemUser — стандартная модель Django для авторизации (с хешированием)
# MyUser — твоя кастомная модель из models.py
from django.contrib.auth.models import User as SystemUser
from .models import Users as MyUser, Posts, Comments, Media, Likes, Follows, RefreshTokens

# ИМПОРТ СЕРИАЛИЗАТОРОВ
from .serializers import (
    UsersSerializer, PostsSerializer, CommentsSerializer, 
    MediaSerializer, LikesSerializer, FollowsSerializer, 
    RefreshTokensSerializer, PostSerializer
)

from .pagination import CustomPageNumberPagination

# --- РЕГИСТРАЦИЯ ---
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка существования в системной таблице
        if SystemUser.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Создаем системного юзера (пароль будет автоматически захеширован)
        SystemUser.objects.create_user(
            username=username, 
            password=password, 
            email=email
        )

        # 2. Создаем запись в твоей таблице (MyUser)
        MyUser.objects.create(
            username=username,
            email=email,
            password=password 
        )

        return Response({"message": "Success! User created in both tables."}, status=status.HTTP_201_CREATED)

# --- ПОСТЫ ---
class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        # Привязываем автора поста к текущему залогиненному юзеру
        serializer.save(author=self.request.user)

class PostListAPIView(generics.ListAPIView):
    queryset = Posts.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination

# --- ОСТАЛЬНЫЕ ВЬЮСЕТЫ ---
class UsersViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer

class FollowsViewSet(viewsets.ModelViewSet):
    queryset = Follows.objects.all()
    serializer_class = FollowsSerializer

class RefreshTokensViewSet(viewsets.ModelViewSet):
    queryset = RefreshTokens.objects.all()
    serializer_class = RefreshTokensSerializer