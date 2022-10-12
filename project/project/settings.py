import os
import datetime
import django

from django.utils.encoding import smart_str

from typing import Union,Any
from pathlib import Path
from decouple import config, Csv

django.utils.encoding.smart_text = smart_str

BASE_DIR = Path(__file__).resolve().parent.parent

# Internationalization
LANGUAGE_CODE: str = config('LANGUAGE_CODE', cast = str)

TIME_ZONE: str = config('TIME_ZONE', cast = str)
USE_I18N: bool = config('USE_I18N', cast = bool)
USE_TZ: bool = config('USE_TZ', cast = bool)

DEFAULT_AUTO_FIELDL: str = 'django.db.models.BigAutoField'

CODE_EXPIRE_MINUTES_TIME: int = config('CODE_EXPIRE_MINUTES_TIME', cast = int)
# Static files
STATIC_URL: str = '/api/static/'
STATIC_ROOT: str = os.path.join(BASE_DIR, 'static/')

PAGINATION_PAGE_SIZE = config('PAGINATION_PAGE_SIZE', cast = int)

SECRET_KEY: str = config('SECRET_KEY', cast = str)

WSGI_APPLICATION: str = 'project.wsgi.application'
ASGI_APPLICATION: str = 'project.asgi.application'

ROOT_URLCONF: str = 'project.urls'

DEBUG: bool = config('DEBUG', cast = bool)

AUTH_USER_MODEL: str = config('AUTH_USER_MODEL', cast = str)

ALLOWED_HOSTS: list[str] = config('ALLOWED_HOSTS', cast = Csv())

# Application definition:
INSTALLED_APPS: tuple[str] = (
    # Default django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Other libs apps:
    'corsheaders',
    'rest_framework_swagger',
    'rest_framework',
    'django_inlinecss',
    'drf_yasg',
    'django_filters',
    'phonenumber_field',
    'channels',
    'storages',
    #My apps:
    'events.apps.EventsConfig',
    'authentication.apps.AuthenticationConfig',
    'notifications.apps.NotificationsConfig',
    'reviews.apps.ReviewsConfig',
)


MIDDLEWARE: tuple[str] = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


#conected datdabse settings
if os.environ.get('GITHUB_WORKFLOW'):
    CELERY_BROKER_URL: str = 'redis://127.0.0.1:6379'
    CELERY_RESULT_BACKEND: str = 'redis://127.0.0.1:6379'
    DATABASES: dict[str, Any]= {
        'default': {
           'ENGINE': config('DB_ENGINE', cast = str),
           'NAME': config('POSTGRES_DB_TEST', cast = str),
           'USER': config('POSTGRES_USER_TEST', cast = str),
           'PASSWORD': config('POSTGRES_PASSWORD_TEST', cast = str),
           'HOST': '127.0.0.1',
           'PORT': config('POSTGRES_PORT', cast = int),
        }
    }
    CHANNEL_LAYERS: dict[str, Any] = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [('127.0.0.1', config('REDIS_PORT', cast = int))],
            },
        },
    }
else:
    CELERY_BROKER_URL: str = config('CELERY_BROKER_URL', cast = str)
    CELERY_RESULT_BACKEND: str = config('CELERY_RESULT_BACKEND', cast = str)
    DATABASES: dict[str,Any] = {
        'default': {
            'ENGINE':config('DB_ENGINE', cast = str),
            'NAME': config('POSTGRES_DB', cast = str),
            'USER': config('POSTGRES_USER', cast = str),
            'PASSWORD': config('POSTGRES_PASSWORD', cast = str),
            'HOST': config('POSTGRES_HOST', cast = str),
            'PORT': config('POSTGRES_PORT', cast = int),
        }
    }
    CHANNEL_LAYERS: dict[str, Any] = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [('redis', config('REDIS_PORT', cast = int))],
            },
        },
    }



SWAGGER_SETTINGS: dict[str, Any] = {
    'SHOW_REQUEST_HEADERS': config('SHOW_REQUEST_HEADERS', cast = bool),
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'Header'
        }
    },
    'USE_SESSION_AUTH': config('USE_SESSION_AUTH', cast = bool),
    'JSON_EDITOR': config('JSON_EDITOR', cast = bool),
    'SUPPORTED_SUBMIT_METHODS': (
        'get',
        'post',
        'put',
        'delete',
    ),
}



TEMPLATES: list[dict[str,Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


AUTH_PASSWORD_VALIDATORS: tuple[dict[str, str]] = (
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
)

REST_FRAMEWORK: dict[str, Any]  = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

SIMPLE_JWT: dict[str, Any] = {
    'AUTH_HEADER_TYPES': (config('AUTH_HEADER_TYPES', cast = str)),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days = config('ACCESS_TOKEN_LIFETIME', cast = int)),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days = config('REFRESH_TOKEN_LIFETIME', cast = int)),
}


#conected smpt gmail settings
EMAIL_BACKEND: str = config('EMAIL_BACKEND', cast = str)
EMAIL_HOST: str = config('EMAIL_HOST', cast = str)
EMAIL_PORT: int = config('EMAIL_PORT', cast = int)
EMAIL_USE_TLS: bool = config('EMAIL_USE_TLS', cast = bool)
EMAIL_HOST_USER: str = config('EMAIL_HOST_USER', cast = str)
EMAIL_HOST_PASSWORD: str = config('EMAIL_HOST_PASSWORD', cast = str)

#celery framework settings
CELERY_TASK_SERIALIZER: str = 'json'
CELERY_RESULT_SERIALIZER: str = 'json'
CELERY_ACKS_LATE: bool = True
CELERY_PREFETCH_MULTIPLIER: int = 1

INTERNAL_IPS: list[str] = config('ALLOWED_HOSTS', cast = Csv())


DEFAULT_FILE_STORAGE: str = config('FILE_STORAGE', cast = str)
FTP_USER: str = config('FTP_USER', cast = str)
FTP_PASS: str = config('FTP_PASS', cast = str)
FTP_PORT: str = config('FTP_PORT', cast = str)
FTP_STORAGE_LOCATION: str = 'ftp://' + FTP_USER + ':' + FTP_PASS + '@ftp-server:' + FTP_PORT

ALGORITHM: str = config('ALGORITHM', cast = str)

CORS_ALLOWED_ORIGINS: tuple[str] = config('CORS_ALLOWED_ORIGINS', cast = Csv())
CORS_ALLOW_METHODS: tuple[str] = config('CORS_ALLOW_METHODS', cast = Csv())
CORS_ALLOW_HEADERS: tuple[str] = config('CORS_ALLOW_HEADERS', cast = Csv())

