"""
Django settings for DigitSoftProyecto project.
...
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# ...

SECRET_KEY = 'django-insecure-7_5cqz@o8t0@z!_+qg!+ddq%!pf!r%y*ooolu&m7!8!y)9hu*)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicaciones principales del proyecto
    'DigitSoft',  # Aplicación principal (frontend público)
    'administrador',  # Dashboard administrativo
    'autenticacion',  # Sistema de autenticación y gestión de usuarios

    # Módulos de negocio (organizados modularmente)
    'clientes',  # Gestión de clientes
    'proveedores',  # Gestión de proveedores
    'inventario',  # Gestión de productos, marcas y equipos
    'ventas',  # Gestión de ventas y carritos
    'compras',  # Gestión de compras y técnicos
    'servicios',  # Gestión de servicios técnicos y órdenes
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DigitSoftProyecto.urls'

# 🟢 CORRECCIÓN CLAVE 1: CONFIGURACIÓN DE TEMPLATES
# Añadimos la ruta de los templates principales (BASE_DIR / 'templates')
# y confiamos en APP_DIRS para encontrar los templates dentro de cada aplicación.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS vacío o apuntando a una carpeta 'templates' global bajo el proyecto.
        # Si tienes 'base.html' en DigitSoft/templates/DigitSoft/, el APP_DIRS True lo encontrará.
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

WSGI_APPLICATION = 'DigitSoftProyecto.wsgi.application'


# Database
# ...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# ...

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# ...

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# ...

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'DigitSoft' / 'static',
]

#Media files (Uploaded by users - Product images, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# ...

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración del correo electrónico
# MODO DESARROLLO: Los correos se muestran en la consola del servidor
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Para producción, descomenta las siguientes líneas y configura tus credenciales:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'jorgedavidcristanchoguarin@gmail.com'
# EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicacion_de_gmail_aqui'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEFAULT_FROM_EMAIL = 'noreply@digitsoft.com'

# Configuración de autenticación
LOGIN_URL = '/autenticacion/login/'
LOGIN_REDIRECT_URL = '/administrador/dashboard/'
LOGOUT_REDIRECT_URL = '/autenticacion/login/'
