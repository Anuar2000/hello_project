from rest_framework import serializers
from .models import Users, Posts, Comments, Media, Likes, Follows, RefreshTokens

class PostSerializer(serializers.ModelSerializer):
    # Добавляем read_only=True. Теперь сериализатор не будет требовать это поле в POST запросе.
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Posts
        fields = ['id', 'author', 'caption', 'created_at']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'

class FollowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follows
        fields = '__all__'

class RefreshTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshTokens
        fields = '__all__'
