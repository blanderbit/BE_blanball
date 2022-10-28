import os

from typing import Any

from decouple import config


if os.environ.get('GITHUB_WORKFLOW'):
    REDIS_HOST: str = '127.0.0.1'
else:
    REDIS_HOST: str = config('REDIS_HOST')

DATABASES: dict[str, Any] = {
    'default': {
        'ENGINE': config('DB_ENGINE', cast = str, 
            default = 'django.db.backends.postgresql_psycopg2'),
        'NAME': config('POSTGRES_DB', cast = str, 
            default = 'postgres_test'),
        'USER': config('POSTGRES_USER', cast = str, 
            default = 'postgres_test'),
        'PASSWORD': config('POSTGRES_PASSWORD', cast = str, 
            default = 'postgres_test'),
        'HOST': config('POSTGRES_HOST', cast = str, 
            default = '127.0.0.1'),
        'PORT': config('POSTGRES_PORT', cast = int,
            default = 5432),
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