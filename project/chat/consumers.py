import json
from typing import Any, Literal, Optional

from authentication.models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import (
    AsyncWebsocketConsumer,
)
from django.utils import timezone


class UserChatConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        if await self.check_user():
            self.user_group_name = await self.room_groop_name()
            self.room_group_name = self.user_group_name

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            if await self.check_user_group_name():
                await self.accept()

    @database_sync_to_async
    def check_user(self) -> Optional[Literal[True]]:
        return User.get_all().filter(email=self.scope["user"]).exists()

    @database_sync_to_async
    def check_user_group_name(self) -> Optional[Literal[True]]:
        user: User = User.get_all().filter(email=self.scope["user"])
        return user[0].chat_group_name == self.room_group_name

    @database_sync_to_async
    def room_groop_name(self) -> User:
        return User.objects.get(email=self.scope["user"]).chat_group_name

    async def disconnect(self, close_code: int) -> None:
        # Leave room group
        if await self.check_user():
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def send_message(self, event: dict[str, Any]) -> None:
        # Send message to WebSocket
        text_data: bytes = json.dumps(
            {"message": event["message"], "date_time": str(timezone.now())},
            ensure_ascii=False,
        ).encode("utf-8")

        await self.send(text_data.decode())
