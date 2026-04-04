import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_project.settings')
django.setup()

from api.models import Users # Убедись, что путь к модели верный

def create_admin():
    username = 'admin'
    email = 'admin@example.com'
    password = 'твой_очень_сложный_пароль' # ЗАМЕНИ НА СВОЙ
    
    if not Users.objects.filter(username=username).exists():
        Users.objects.create_superuser(username=username, email=email, password=password)
        print(f"Суперпользователь {username} создан!")
    else:
        print(f"Пользователь {username} уже существует.")

if __name__ == '__main__':
    create_admin()