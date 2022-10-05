import os
import django
import jwt

from datetime import datetime
from typing import Any,Union
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from authentication.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

ALGORITHM: str = "HS256"

@database_sync_to_async
def get_user(token: str) -> Union[AnonymousUser, User]:
    try:
        payload: dict[str, Any] = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except User.DoesNotExist:
        return AnonymousUser()

    token_exp: datetime = datetime.fromtimestamp(payload['exp'])
    if token_exp < datetime.utcnow():
        return AnonymousUser()

    try:
        user: User = User.objects.get(id=payload['user_id'])
    except User.DoesNotExist:
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope: dict, receive, send) -> Union[ValueError, OrderedDict]:
        close_old_connections()
        try:
            token_key: str = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
    
        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)