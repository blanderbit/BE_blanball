import os

from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


django_asgi_app = get_asgi_application()
import notifications.routing
from authentication.middlewares import (
    JwtAuthMiddlewareStack,
)

application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(
                URLRouter(notifications.routing.websocket_urlpatterns)
            )
        ),
        "http": django_asgi_app,
    }
)
