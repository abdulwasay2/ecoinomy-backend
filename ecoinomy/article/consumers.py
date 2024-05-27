import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class OrderConsumer(WebsocketConsumer):
    def connect(self):
        # Parse query_string
        if not self.scope['user'].is_authenticated:
            self.close(code=4001)

        self.user = self.scope['user']
        self.room_group_name = f'cart_update_room_{self.user.id}'
        
        self.accept()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json["data"]

        # TODO: Add logic for asking for an update

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "order_update", "data": message}
        )

    # Receive message from room group
    def order_update(self, event):
        message = event["data"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"data": message}))