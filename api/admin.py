from django.contrib import admin
from .models import User, Post, Comment, Like, Follow, Media, RefreshToken

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Media)
admin.site.register(RefreshToken)