from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # все эндпоинты будут начинаться с /api/
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', TemplateView.as_view(template_name='index.html'))
]
