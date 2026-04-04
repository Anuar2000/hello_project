import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_project.settings')
django.setup()

from api.models import Users

def create_admin():
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin' 
    
    Users.objects.filter(username=username).delete()

    admin_user = Users.objects.create_superuser(
        username=username, 
        email=email, 
        password=password
    )

    print(f"User {admin_user.username} created.")
    print(f"Is staff: {admin_user.is_staff}")
    print(f"Password hash starts with: {admin_user.password[:10]}")

if __name__ == '__main__':
    create_admin()