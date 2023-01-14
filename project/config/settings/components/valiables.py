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


# maximum file weight in kilobytes for uploading a user avatar to profile
FILE_UPLOAD_MAX_MEMORY_SIZE: int = 1024

# project secret key
SECRET_KEY: str = config("SECRET_KEY", cast=str)

# list of allowed project hosts
ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", cast=Csv())
################################################################

# the path where you can open any static file 
# from the directory STATIC_ROOT in the browser
STATIC_URL: str = "/api/static/"

# the path to the folder where all static files, styles, etc. are saved
STATIC_ROOT: str = path.join(settings._BASE_DIR, "static/")

# path to the file that is responsible 
# for processing synchronous requests to the application
WSGI_APPLICATION: str = "config.wsgi.application"
# path to the file that is responsible for 
# processing asynchronous requests to the application

ASGI_APPLICATION: str = "config.asgi.application"

# path to a file that contains all the application's routing paths
ROOT_URLCONF: str = "config.urls"

# the constant that is responsible for which 
# locale is currently set in the application
LANGUAGE_CODE: str = config("LANGUAGE_CODE", cast=str)

# the constant responsible for the time 
# zone in which the application will work
TIME_ZONE: str = config("TIME_ZONE", cast=str)

USE_I18N: bool = config("USE_I18N", cast=bool)

USE_TZ: bool = False

USE_L10N: bool = True

# the constant that is responsible for filling the id field
DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

# number of items to be displayed on list pages
PAGINATION_PAGE_SIZE: int = config("PAGINATION_PAGE_SIZE", cast=int)

# main user model
AUTH_USER_MODEL: str = config("AUTH_USER_MODEL", cast=str)

# the number of minutes the lifetime of the confirmation 
# code for various actions, reset email, password, etc.
CODE_EXPIRE_MINUTES_TIME: int = config("CODE_EXPIRE_MINUTES_TIME", cast=int)


# the algorithm by which the token 
# for the websocket connection is hashed
ALGORITHM: str = config("ALGORITHM", cast=str)

# the constant that is responsible for the mode in which the application will work. 
# if true will be the development mode.
# if false, then in prod server mode
DEBUG: bool = config("DEBUG", cast=bool)

if DEBUG == False:
    # host where all pictures uploaded by users are located
    MINIO_IMAGE_HOST: str = getenv("MINIO_IMAGE_HOST_PROD")
else:
    MINIO_IMAGE_HOST: str = getenv("MINIO_IMAGE_HOST")

# secret key from NOVAPOSHTA api, by which we get a list of cities in Ukraine
NOVAPOSHTA_API_KEY: str = config("NOVAPOSHTA_API_KEY", cast=str)

# maximum API key length
API_KEY_MAX_LENGTH: int = 255
