# Scaffolding: Django + DRF + JWT + PostgreSQL
### Estilo nativo Django (Django Way) · DSD-2303

> **¿Cuándo usar este enfoque?**  
> Proyectos donde la lógica de negocio es directa y el ORM de Django hace el trabajo sin necesidad de abstracciones extra. Es el estilo que encontrarás en la documentación oficial de Django y en la mayoría de tutoriales.

---

## Diferencia clave vs. arquitectura multicapa

| | Django Way | Multicapa |
|---|---|---|
| Acceso a BD | ORM directo en la view | Via Repository |
| Lógica de negocio | En el Model o en la View | En Services separados |
| Archivos por app | 5 (los que genera Django) | 7+ (+ services, repositories) |
| Ideal para | CRUDs estándar, prototipos | Lógica compleja, apps grandes |
| ViewSet | `ModelViewSet` (automático) | `APIView` (manual) |

---

## Stack

| Componente | Versión recomendada |
|---|---|
| Python | 3.12+ |
| Django | 5.x |
| djangorestframework | 3.15+ |
| djangorestframework-simplejwt | 5.x |
| drf-spectacular | 0.27+ |
| psycopg2-binary | 2.9+ |
| python-dotenv | 1.x |
| django-cors-headers | 4.x |

---

## Estructura de Carpetas

```
mi_proyecto/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── __init__.py
│   └── users/
│       ├── __init__.py
│       ├── models.py         ← Esquema + puede tener métodos de negocio simples
│       ├── serializers.py    ← Validación y serialización    ⚠️ crear manualmente
│       ├── views.py          ← ViewSets: lógica + acceso a BD en un lugar
│       ├── urls.py           ← Router automático              ⚠️ crear manualmente
│       ├── admin.py
│       └── apps.py
│
├── .env
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## Paso a Paso

### 1. Entorno virtual y dependencias

```bash
mkdir mi_proyecto && cd mi_proyecto

python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install django djangorestframework \
            djangorestframework-simplejwt \
            drf-spectacular \
            psycopg2-binary python-dotenv \
            django-cors-headers

pip freeze > requirements.txt
```

### 2. Scaffolding del proyecto

```bash
django-admin startproject config .

mkdir apps
touch apps/__init__.py

# Crear la primera app directamente en apps/
python manage.py startapp users apps/users

touch apps/users/serializers.py
touch apps/users/urls.py

touch .env .env.example .gitignore
```

---

## Archivos de Configuración

### `.env`
```ini
SECRET_KEY=MySecretKeyForDjangoApp
DEBUG=True
DB_NAME=django_db
DB_USER=testuser
DB_PASSWORD=testuser
DB_HOST=localhost
DB_PORT=5432
APP_NAME=My Django App
APP_DESCRIPTION=A simple Django app
APP_VERSION=1.0.0
```

> ⚠️ La contraseña **no debe contener caracteres especiales** (acentos, ñ, símbolos). Usa solo letras, números, guiones y guiones bajos. PostgreSQL y psycopg2 pueden fallar al conectarse si la contraseña contiene caracteres fuera del rango ASCII.

### `.env.example`
```ini
SECRET_KEY=
DEBUG=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
APP_NAME=
APP_DESCRIPTION=
APP_VERSION=
```

### `.gitignore`
```
venv/
__pycache__/
*.pyc
.env
*.sqlite3
.DS_Store
```

### `config/settings.py`

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    # Nuestras apps
    'apps.users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← Debe ir primero
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     os.getenv('DB_NAME'),
        'USER':     os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST':     os.getenv('DB_HOST', 'localhost'),
        'PORT':     os.getenv('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF: JWT por defecto
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':  True,
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': os.getenv('API_TITLE', 'Mi API'),
    'DESCRIPTION': os.getenv('API_DESCRIPTION', 'Documentación de la API'),
    'VERSION': os.getenv('API_VERSION', '1.0.0'),
    'SERVE_INCLUDE_SCHEMA': False,
}

# CORS (solo desarrollo)
CORS_ALLOW_ALL_ORIGINS = True
```

### `apps/users/apps.py`

```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'  # ← Ruta completa
```

### `config/urls.py`

```python
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

# Rutas versionadas — cada versión incluye su propio urls.py
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
```

> **¿Por qué Swagger fuera de `/api/v1/`?**
> La documentación describe *toda* la API. Mantenerla sin versión en `/api/docs/` evita duplicar rutas de documentación cuando se agregue `v2`.

---

## Esqueleto de Capas — Django Way

### `models.py`
```python
from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = 'users'
        ordering  = ['-created_at']

    def __str__(self):
        return self.email

    def deactivate(self):
        self.is_active = False
        self.save()
```

### `serializers.py`
```python
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'name', 'email', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
```

### `views.py`
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset         = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.deactivate()
        return Response({'status': 'usuario desactivado'})
```

### `urls.py`
```python
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls
```

---

## Verificación Final

```bash
python manage.py migrate
python manage.py runserver
```

- `http://127.0.0.1:8000/api/v1/auth/login/` → `405 Method Not Allowed` ✅
- `http://127.0.0.1:8000/api/docs/` → Swagger UI carga correctamente ✅
- `http://127.0.0.1:8000/admin/` → Django Admin carga correctamente ✅

---

## Endpoints disponibles tras el scaffolding

| Método | URL | Acción | Auth |
|--------|-----|--------|------|
| POST | `/api/v1/auth/login/` | Obtener tokens | No |
| POST | `/api/v1/auth/refresh/` | Renovar access token | No |
| GET | `/api/schema/` | Esquema OpenAPI (JSON/YAML) | No |
| GET | `/api/docs/` | Swagger UI interactivo | No |
| GET | `/api/v1/users/` | Listar usuarios | JWT |
| POST | `/api/v1/users/` | Crear usuario | JWT |
| GET | `/api/v1/users/{id}/` | Ver usuario | JWT |
| PUT | `/api/v1/users/{id}/` | Actualizar completo | JWT |
| PATCH | `/api/v1/users/{id}/` | Actualizar parcial | JWT |
| DELETE | `/api/v1/users/{id}/` | Eliminar | JWT |
| POST | `/api/v1/users/{id}/deactivate/` | Acción personalizada | JWT |

> Cuando el proyecto crezca y necesite una `v2`, basta con agregar `path('api/v2/', include((v2_patterns, 'v2')))` en `urls.py` sin romper los clientes que usan `v1`.

---

## ¿Cuándo preferir cada enfoque?

| Situación | Recomendación |
|---|---|
| CRUD estándar sin reglas complejas | **Django Way** |
| Prototipo rápido | **Django Way** |
| Reglas de negocio elaboradas (descuentos, flujos, cálculos) | **Multicapa** |
| Equipo grande, necesidad de testear capas por separado | **Multicapa** |
| App que puede crecer mucho | **Multicapa** |

---

*DSD-2303 · Desarrollo de Servicios Web · Instituto Tecnológico de Oaxaca*
