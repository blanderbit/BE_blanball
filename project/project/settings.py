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
LANGUAGE_CODE:str = config('LANGUAGE_CODE')

TIME_ZONE:str = config('TIME_ZONE')
USE_I18N:bool = config('USE_I18N',cast = bool,default = True)
USE_TZ:bool = config('USE_TZ',cast = bool,default = True)

DEFAULT_AUTO_FIELDL:str = 'django.db.models.BigAutoField'


# Static files
STATIC_URL:str = '/static/'
STATIC_ROOT:str = os.path.join(BASE_DIR,'static')

MEDIA_URL:str = '/media/'
MEDIA_ROOT:str = os.path.join(BASE_DIR,'media')

SECRET_KEY:str = config('SECRET_KEY')

WSGI_APPLICATION:str = 'project.wsgi.application'
ASGI_APPLICATION:str = 'project.asgi.application'

ROOT_URLCONF:str = 'project.urls'

DEBUG:bool = config('DEBUG',cast = bool,default = True)

AUTH_USER_MODEL:str = config('AUTH_USER_MODEL')

ALLOWED_HOSTS:list[str] = config('ALLOWED_HOSTS', cast=Csv())

# Application definition:
INSTALLED_APPS:tuple[str] = (
    # Default django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Other libs apps:
    'rest_framework_swagger',
    'rest_framework',
    'django_inlinecss',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'drf_yasg',
    'django_filters',
    'phonenumber_field',
    'channels',

    #My apps:
    'events.apps.EventsConfig',
    'authentication.apps.AuthenticationConfig',
    'notifications.apps.NotificationsConfig',
    'reviews.apps.ReviewsConfig',
)

ELASTICSEARCH_DSL:dict[str,Any] = {
    'default': {
        'hosts': 'elasticsearch:9200',
    }
}

MIDDLEWARE:tuple[str] = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


#POSTGRES conected datdabse settings

DATABASES:dict[str,Any] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),
    }
}

CHANNEL_LAYERS:dict[str,Any] = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis",config('REDIS_PORT'))],
        },
    },
}


SWAGGER_SETTINGS:dict[str,Union[str,dict[str,Any]]] = {
    'SHOW_REQUEST_HEADERS': config('SHOW_REQUEST_HEADERS',cast = bool),
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'Header'
        }
    },
    'USE_SESSION_AUTH': config('USE_SESSION_AUTH',cast = bool),
    'JSON_EDITOR': config('JSON_EDITOR',cast = bool),
    'SUPPORTED_SUBMIT_METHODS': (
        'get',
        'post',
        'put',
        'delete',
    ),
}



TEMPLATES:list[dict[str,Any]] = [
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


AUTH_PASSWORD_VALIDATORS:tuple[dict[str,str]] = (
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

REST_FRAMEWORK:dict[str,Any]  = {
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

SIMPLE_JWT:dict[str,Any] = {
    'AUTH_HEADER_TYPES': (config('AUTH_HEADER_TYPES')),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=config('ACCESS_TOKEN_LIFETIME',cast = int)),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=config('REFRESH_TOKEN_LIFETIME',cast = int)),
}


#conected smpt gmail settings
EMAIL_BACKEND:str='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST:str = config('EMAIL_HOST')
EMAIL_PORT:int = config('EMAIL_PORT',cast = int)
EMAIL_USE_TLS:bool = config('EMAIL_USE_TLS',cast = bool)
EMAIL_HOST_USER:str = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD:str = config('EMAIL_HOST_PASSWORD')

#celery framework settings
CELERY_BROKER_URL:str = config('CELERY_BROKER_URL')
CELERY_BROKER_TRANSPORT_OPTIONS:dict[str,int] = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND:str = config('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = {'application/json'}
CELERY_TASK_SERIALIZER:str = 'json'
CELERY_RESULT_SERIALIZER:str = 'json'
CELERY_ACKS_LATE:bool = True
CELERY_PREFETCH_MULTIPLIER:int = 1
