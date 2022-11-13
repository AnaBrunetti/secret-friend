import json
from django.conf import settings
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import User
from chat.models import ChatRoom, Message

 
class ChatRoomConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def save_message(self, user_id, chat_room_id, message):
        Message.objects.create(
            user_id=user_id,
            chat_room_id=chat_room_id,
            context=message
        )
        
    @database_sync_to_async
    def send_bot_message(self, chat_room_id, message):
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        if chat_room and chat_room.chat.users.filter(role=User.ROLE_BOT).exists():
            bot_id = User.objects.filter(role=User.ROLE_BOT).first().id
            message = settings.BOT_MESSAGE
            return bot_id, message
        return None, None
    
    async def connect(self):
        self.slug = self.scope["url_route"]["kwargs"]["slug"]
        self.group_name = "chat_%s" % self.slug
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user_id"]
        chat_room_id = text_data_json["chat_room_id"]

        await self.save_message(user_id, chat_room_id, message)
        await self.channel_layer.group_send(
            self.group_name,{
                "type" : "chatbox_message",
                "message" : message,
                "user_id": user_id,
                "chat_room_id": chat_room_id,
            })

        bot_id, bot_message = await self.send_bot_message(chat_room_id, message)
        if bot_id and bot_message:
            await self.save_message(bot_id, chat_room_id, bot_message)
            await self.channel_layer.group_send(
                self.group_name,{
                    "type" : "chatbox_message",
                    "message" : bot_message,
                    "user_id": bot_id,
                    "chat_room_id": chat_room_id,
                })

    async def chatbox_message(self , event):
        user_id = event["user_id"]
        chat_room_id = event["chat_room_id"]
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "user_id": user_id,
                    "chat_room_id": chat_room_id,
                    "message": message,
                }
            )
        )
