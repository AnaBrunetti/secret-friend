"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
from chat.consumers import ChatRoomConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<chat_box_name>\w+)/$", ChatRoomConsumer.as_asgi()
    ),
]

application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() ,
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )   
        )
    }
)