"""
ASGI config for High Dashboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# highfeature_dashboard directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "highfeature_dashboard"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# Other explaination in the video "Django Channels Push Notifications [Part-1]" 25:00
# This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()

### USE THIS, to a separate app for websocket
# # Import websocket application here, so apps from django_application are loaded first
# from config.websocket import websocket_application  # noqa isort:skip
#
#
# async def application(scope, receive, send):
#     if scope["type"] == "http":
#         await django_application(scope, receive, send)
#     elif scope["type"] == "websocket":
#         await websocket_application(scope, receive, send)
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")

### OR THIS to an integrated websocket into django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

# Import websocket application here, so apps from django_application are loaded first
from . import urls  # noqa isort:skip


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(urls.websocket_urlpatterns))),
    }
)
