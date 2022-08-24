from channels.generic.websocket import AsyncWebsocketConsumer
import json
from authentication.models import User
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user_obj(self,email):
    return User.objects.get(email=email)

class KafkaConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.event_name = self.scope['url_route']['kwargs']['event_name']
        self.room_group_name = self.event_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(get_user_obj(email = self.scope['user']))
        if get_user_obj(email = self.scope['user']) != None:
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'kafka_message',
                'message': message
            }
        )

    # Receive message from room group
    async def kafka_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))