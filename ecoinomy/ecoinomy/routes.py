from django.urls import re_path

from article import consumers

websocket_urlpatterns = [
    re_path(r"", consumers.OrderConsumer.as_asgi()),
]
