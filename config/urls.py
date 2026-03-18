from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

# API versioning: /api/v1/

v1_patterns = [
    path('auth/login/',   TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('', include('apps.users.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # Versionado: /api/v1/
    path('api/v1/', include((v1_patterns, 'v1'))),
    # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(),                      name='schema'),
    path('api/docs/',   SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]