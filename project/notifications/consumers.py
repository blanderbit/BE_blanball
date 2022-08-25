from channels.generic.websocket import AsyncWebsocketConsumer
import json
from authentication.models import User
from channels.db import database_sync_to_async
from events.models import Event
from .models import Notification


    
class KafkaConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        if await self.check_user(user = self.scope['user']):
            if await self.event_exists():
                await self.add_user_to_room(user = self.scope['user'])
                await self.accept()
                await self.notify_users()
        

    async def disconnect(self,close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.remove_user_from_room(user = self.scope['user'])

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

    @database_sync_to_async
    def check_user(self,user):
        user = user
        if user:
            if not user.current_rooms.filter(name = self.room_group_name).exists():
                return True

    
    @database_sync_to_async
    def add_user_to_room(self,user):
        user = user
        user.current_rooms.add(Event.objects.get(name = self.room_group_name))

    @database_sync_to_async
    def event_exists(self):
        event = Event.objects.filter(name = self.room_group_name)
        if event:
            if event[0].amount_members+1 > len(event[0].current_users.all()):
                return True

    @database_sync_to_async
    def remove_user_from_room(self,user):
        user = user
        user.current_rooms.remove(Event.objects.get(name = self.room_group_name))

    @database_sync_to_async
    def notify_users(self):
        event = Event.objects.get(name = self.room_group_name)
        for user in event.current_users.all():
            Notification.objects.create(user=user,text=f'{user.profile.name} не забывайте')