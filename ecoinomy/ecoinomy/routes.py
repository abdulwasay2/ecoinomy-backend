from django.urls import re_path

from order import consumers

websocket_urlpatterns = [
    re_path(r"", consumers.OrderConsumer.as_asgi()),
]
