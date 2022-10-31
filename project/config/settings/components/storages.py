import os

from typing import Any

from decouple import config


if os.environ.get('GITHUB_WORKFLOW'):
    REDIS_HOST: str = '127.0.0.1'

    DATABASES: dict[str, Any] = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres_test',
            'USER': 'postgres_test',
            'PASSWORD': 'postgres_test',
            'HOST': '127.0.0.1',
            'PORT': 5432,
        } 
    }
else:
    REDIS_HOST: str = config('REDIS_HOST', cast = str)

    DATABASES: dict[str, Any] = {
        'default': {
            'ENGINE': config('DB_ENGINE', cast = str),
            'NAME': config('DB_NAME', cast = str),
            'USER': config('DB_USER', cast = str),
            'PASSWORD': config('DB_PASSWORD', cast = str),
            'HOST': config('DB_HOST', cast = str),
            'PORT': config('DB_PORT', cast = int),
        }
    }
    
CHANNEL_LAYERS: dict[str, Any] = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, config('REDIS_PORT', cast = int, 
                default = 6379))],
        },
    },
}

DEFAULT_FILE_STORAGE: str = config('FILE_STORAGE', cast = str)
FTP_USER: str = config('FTP_USER', cast = str)
FTP_PASS: str = config('FTP_PASS', cast = str)
FTP_PORT: str = config('FTP_PORT', cast = str)
FTP_STORAGE_LOCATION: str = 'ftp://' + FTP_USER + ':' + FTP_PASS + '@ftp-server:' + FTP_PORT