from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password)
        # Для суперпользователя нужно добавить флаги, если они есть в БД
        user.is_admin = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=32)
    email = models.CharField(unique=True, max_length=255)
    # Используем db_column, чтобы соответствовать существующей колонке
    password = models.CharField(max_length=255, db_column='password_hash')
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        managed = True
        db_table = 'users'

    def has_perm(self, perm, obj=None): return True
    def has_module_perms(self, app_label): return True
    @property
    def is_staff(self): return True

# Остальные модели оставляем как есть, так как они ссылаются на твою таблицу
class Posts(models.Model):
    author = models.ForeignKey('Users', models.DO_NOTHING)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'posts'

class Comments(models.Model):
    post = models.ForeignKey('Posts', models.DO_NOTHING)
    author = models.ForeignKey('Users', models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comments'

class Media(models.Model):
    post = models.ForeignKey('Posts', models.DO_NOTHING)
    url = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=64, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    order_idx = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'media'

class Follows(models.Model):
    follower = models.ForeignKey('Users', models.DO_NOTHING, db_column='follower_id')
    followee = models.ForeignKey('Users', models.DO_NOTHING, related_name='follows_followee_set', db_column='followee_id')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'follows'
        unique_together = (('follower', 'followee'),)

class Likes(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    post = models.ForeignKey('Posts', models.DO_NOTHING, db_column='post_id')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'likes'
        unique_together = (('user', 'post'),)

class RefreshTokens(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    jti = models.CharField(unique=True, max_length=64)
    revoked = models.BooleanField(blank=True, null=True)
    expires_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'refresh_tokens'