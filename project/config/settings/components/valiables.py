from os import getenv, path

import django
from decouple import Csv, config
from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.translation import (
    gettext_lazy as _,
)

django.utils.encoding.smart_text = smart_str


################################################################

# Build paths inside the project like this: BASE_DIR.joinpath('some')
# `pathlib` is better than writing: dirname(dirname(dirname(__file__)))

FILE_UPLOAD_MAX_MEMORY_SIZE: int = 1024

SECRET_KEY: str = config("SECRET_KEY", cast=str)

ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", cast=Csv())
################################################################

STATIC_URL: str = "/api/static/"
STATIC_ROOT: str = path.join(settings._BASE_DIR, "static/")

WSGI_APPLICATION: str = "config.wsgi.application"
ASGI_APPLICATION: str = "config.asgi.application"

ROOT_URLCONF: str = "config.urls"

LANGUAGE_CODE: str = config("LANGUAGE_CODE", cast=str)

TIME_ZONE: str = config("TIME_ZONE", cast=str)
USE_I18N: bool = config("USE_I18N", cast=bool)
USE_TZ: bool = False
USE_L10N: bool = True

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

PAGINATION_PAGE_SIZE: int = config("PAGINATION_PAGE_SIZE", cast=int)

AUTH_USER_MODEL: str = config("AUTH_USER_MODEL", cast=str)

CODE_EXPIRE_MINUTES_TIME: int = config("CODE_EXPIRE_MINUTES_TIME", cast=int)

ALGORITHM: str = config("ALGORITHM", cast=str)

DEBUG: bool = config("DEBUG", cast=bool)

if DEBUG == False:
    MINIO_IMAGE_HOST: str = getenv("MINIO_IMAGE_HOST_PROD")
else:
    MINIO_IMAGE_HOST: str = getenv("MINIO_IMAGE_HOST")

NOVAPOSHTA_API_KEY: str = config("NOVAPOSHTA_API_KEY", cast=str)
