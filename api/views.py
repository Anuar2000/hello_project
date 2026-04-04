from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import status

# ИМПОРТ МОДЕЛЕЙ
# SystemUser — стандартная модель Django для авторизации (с хешированием)
# MyUser — твоя кастомная модель из models.py
from django.contrib.auth.models import User as SystemUser
from .models import Users as MyUser, Posts, Comments, Media, Likes, Follows, RefreshTokens
from .models import Users
from .serializers import (
    UsersSerializer, PostsSerializer, CommentsSerializer, 
    MediaSerializer, LikesSerializer, FollowsSerializer, 
    RefreshTokensSerializer, PostSerializer
)

from .pagination import CustomPageNumberPagination

# --- РЕГИСТРАЦИЯ ---
class RegisterView(APIView):
    """
    Эндпоинт для регистрации новых пользователей.
    Использует кастомную модель Users и MyUserManager.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # Получаем данные из запроса (Android отправляет их в теле JSON)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # 1. Проверка на наличие всех обязательных полей
        if not username or not password or not email:
            return Response(
                {"error": "Необходимо заполнить все поля: username, email, password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Проверка уникальности username
        if Users.objects.filter(username=username).exists():
            return Response(
                {"error": "Пользователь с таким логином уже зарегистрирован"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 3. Проверка уникальности email
        if Users.objects.filter(email=email).exists():
            return Response(
                {"error": "Пользователь с таким email уже зарегистрирован"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 4. Создание пользователя через твой кастомный менеджер
            # Это захеширует пароль и сохранит запись в таблицу 'users'
            user = Users.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            return Response(
                {"message": "Регистрация успешно завершена!"}, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            # Если что-то пойдет не так на уровне БД, мы увидим текст ошибки
            return Response(
                {"error": f"Ошибка при сохранении в базу данных: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        ы
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