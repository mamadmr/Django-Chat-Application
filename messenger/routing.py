from django.urls import re_path
from .consumers import MessageConsumer
from .middleware import WebSocketJWTAuthMiddleware

websocket_urlpatterns = [
    re_path(r'^ws/message/$', WebSocketJWTAuthMiddleware(MessageConsumer.as_asgi())),
]