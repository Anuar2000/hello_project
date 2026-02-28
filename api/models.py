from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# 1. Добавляем менеджер (он нужен для создания юзеров)
class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(username=username, email=email)
        user.set_password(password) # Хэширует пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# 2. Обновляем саму модель
class Users(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=32)
    email = models.CharField(unique=True, max_length=255)
    # Используем db_column, чтобы Django писал пароль в твою колонку password_hash
    password = models.CharField(max_length=255, db_column='password_hash')
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username' # Критически важно!
    REQUIRED_FIELDS = ['email']

    class Meta:
        managed = False
        db_table = 'users'

    # Добавь эти методы, чтобы Django не ругался при создании суперпользователя
    def has_perm(self, perm, obj=None): return True
    def has_module_perms(self, app_label): return True
    @property
    def is_staff(self): return True

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Comments(models.Model):
    post = models.ForeignKey('Posts', models.DO_NOTHING)
    author = models.ForeignKey('Users', models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Follows(models.Model):
    pk = models.CompositePrimaryKey('follower_id', 'followee_id')
    follower = models.ForeignKey('Users', models.DO_NOTHING)
    followee = models.ForeignKey('Users', models.DO_NOTHING, related_name='follows_followee_set')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'follows'


class Likes(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'post_id')
    user = models.ForeignKey('Users', models.DO_NOTHING)
    post = models.ForeignKey('Posts', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'likes'


class Media(models.Model):
    post = models.ForeignKey('Posts', models.DO_NOTHING)
    url = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=64, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    order_idx = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media'


class Posts(models.Model):
    author = models.ForeignKey('Users', models.DO_NOTHING)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'posts'


class RefreshTokens(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    jti = models.CharField(unique=True, max_length=64)
    revoked = models.BooleanField(blank=True, null=True)
    expires_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'refresh_tokens'
