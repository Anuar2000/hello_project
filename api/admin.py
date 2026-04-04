from django.contrib import admin
from .models import Users, Posts, Comments, Likes, Follows, Media, RefreshTokens

admin.site.register(Users)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Follows)
admin.site.register(Media)
admin.site.register(RefreshTokens)