from channels.generic.websocket import AsyncWebsocketConsumer
import json
from authentication.models import User
from channels.db import database_sync_to_async
from events.models import Event
from .tasks import *
    
class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_group_name = self.scope['url_route']['kwargs']['user_group_name']
        self.room_group_name = self.user_group_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        if await self.check_user(user_email = self.scope['user']):
            await self.accept()

    @database_sync_to_async
    def check_user(self,user_email):
        user = User.objects.filter(email = user_email)
        if user:
            if user[0].group_name == self.room_group_name:
                return True

    async def disconnect(self,close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

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


    async def kafka_message(self, event):
        # Send message to WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))