import json
from types import NoneType
from typing import Any, Optional, Literal

from authentication.models import (
    User,
)

from django.utils import timezone

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
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
    def check_user(self) -> Optional[Literal[True]]:
        user: User = User.objects.filter(email = self.scope['user'])
        if user:
            return True

    @database_sync_to_async
    def check_user_group_name(self) -> Optional[Literal[True]]:
        user: User = User.objects.filter(email = self.scope['user'])
        if user[0].group_name ==  self.room_group_name:
            return True

    @database_sync_to_async
    def room_groop_name(self) -> User:
        return User.objects.get(email = self.scope['user']).group_name

    @database_sync_to_async
    def add_user_to_active(self) -> None:
        self.disconnect(200)
        user: User = User.objects.get(email = self.scope['user'])
        user.is_online = True
        user.save()

    @database_sync_to_async
    def delete_user_from_active(self) -> None:
        user: User = User.objects.get(email = self.scope['user'])
        user.is_online = False
        user.save()

    async def disconnect(self, close_code: int) -> None:
        # Leave room group
        if await self.check_user():
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            await self.delete_user_from_active()

    async def kafka_message(self, event: dict[str, Any]) -> None:
        # Send message to WebSocket
        text_data: bytes = json.dumps({
            'date_time': str(timezone.now()),
            'message_type': event['message_type'],
            'notification_id': event['notification_id'],
            'data': event['data']
        }, ensure_ascii = False).encode('utf-8')

        await self.send(text_data.decode())
