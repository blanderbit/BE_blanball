import json

from .tasks import *
from authentication.models import User,ActiveUser

from django.utils import timezone

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin


class UserConsumer(ObserverModelInstanceMixin,AsyncWebsocketConsumer):
    async def connect(self):
        if await self.check_user():
            self.user_group_name = await self.room_groop_name()
            self.room_group_name = self.user_group_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            if await self.check_user_group_name():
                await self.accept()
                await self.add_user_to_active()

    @database_sync_to_async
    def check_user(self) -> bool:
        user = User.objects.filter(email = self.scope['user'])
        if user:
            return True

    @database_sync_to_async
    def check_user_group_name(self):
        user = User.objects.filter(email = self.scope['user'])
        if user[0].group_name ==  self.room_group_name:
            return True

    @database_sync_to_async
    def room_groop_name(self) -> str:
        return User.objects.get(email = self.scope['user']).group_name

    @database_sync_to_async
    def add_user_to_active(self):
        self.disconnect(400)
        ActiveUser.objects.filter(user = User.objects.get(email = self.scope['user']).id).delete()
        ActiveUser.objects.create(user = User.objects.get(email = self.scope['user']))

    @database_sync_to_async
    def delete_user_from_active(self):
        return ActiveUser.objects.filter(user = User.objects.get(email = self.scope['user']).id).delete()

    async def disconnect(self,close_code):
        # Leave room group
        if await self.check_user():
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print(type(await self.delete_user_from_active()))
            return await self.delete_user_from_active()

    async def kafka_message(self, event):
        # Send message to WebSocket
        message = event['message']
        message_type =  event['message_type']
        await self.send(text_data=json.dumps({
            'message': message,
            'date_time': str(timezone.now()),
            'message_type':message_type,
        }))
