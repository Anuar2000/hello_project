from rest_framework import viewsets
from rest_framework import generics
from .pagination import CustomPageNumberPagination
from .models import Users, Posts, Comments, Media, Likes, Follows, RefreshTokens
from .serializers import UsersSerializer, PostsSerializer, CommentsSerializer, MediaSerializer, LikesSerializer, FollowsSerializer, RefreshTokensSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    
    # ПРОВЕРЬ ТУТ: множественное число, с буквой 's' на конце!
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        # Если ты зайдешь без токена, эта строка вызовет ошибку, 
        # так как в request.user будет аноним, а не твой админ
        serializer.save(author=self.request.user)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
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

class PostListAPIView(generics.ListAPIView):
    queryset = Posts.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Логин и пароль обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Пользователь с таким именем уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        # ВОТ ТУТ МАГИЯ: create_user автоматически хеширует пароль
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return Response({"message": "Пользователь успешно создан"}, status=status.HTTP_201_CREATED)