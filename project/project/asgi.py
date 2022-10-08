import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import notifications.routing
from authentication.middlewares import  JwtAuthMiddlewareStack


application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": JwtAuthMiddlewareStack(URLRouter(
        notifications.routing.websocket_urlpatterns
    )
  )
})
 