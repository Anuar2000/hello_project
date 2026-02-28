from rest_framework import viewsets
from .models import Users, Posts, Comments, Media, Likes, Follows, RefreshTokens
from .serializers import UsersSerializer, PostsSerializer, CommentsSerializer, MediaSerializer, LikesSerializer, FollowsSerializer, RefreshTokensSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer

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
