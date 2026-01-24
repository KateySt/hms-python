import json
from datetime import datetime
from typing import Any

from channels.generic.websocket import AsyncWebsocketConsumer


class ChartConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chart_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data: str | None = None) -> None:
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if not message:
            await self.send(text_data=json.dumps({"message": "Message is required"}))
            return

        user = self.scope["user"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": user.email,
                "timestamp": datetime.now().isoformat(),
            },
        )

    async def chat_message(self, event: dict[str, Any]) -> None:
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "timestamp": timestamp,
                }
            )
        )
