from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/chat/<room_uuid>/", consumers.ChatConsumer.as_asgi()),
]
