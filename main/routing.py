from chat.consumers import ChatRoomConsumer
from django.urls import re_path
 
websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<slug>[^/]+)/$", ChatRoomConsumer.as_asgi()
    ),
]