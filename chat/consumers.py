import json
from channels.generic.websocket import AsyncWebsocketConsumer
from intra import settings
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chatterbot = ChatBot(**settings.CHATTERBOT)
        if self.groups is None:
            self.groups = []

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

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
        # response = self.chatterbot.get_response(message)
        # response_data = response.serialize()


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                # 'message': response_data["text"]
                 'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print("Recibe1")
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))