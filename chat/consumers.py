from channels.generic.websocket import WebsocketConsumer

import json
from asgiref.sync import async_to_sync

from .models import Message
from .serializers import MessageSerializer
from .helpers import send_message_to_admin

from .models import Chat
from users.models import User

from django.utils import timezone


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.user = get_user_from_token(self.scope["url_route"]["kwargs"]["token"])
        user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.user = User.objects.get(pk=user_id)
        self.room_name = user_id

        # # Reject the request if user isn't admin and trying to connect to another user socket
        # if str(self.user.pk) != str(self.room_name) \
        # and not self.user.is_staff \
        # and not self.user.is_superuser:
        #     self.close()

        self.room_group_name = f"chat_{self.room_name}"

        self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = {}

        # if sent data is seen
        if text_data_json.get("seen_by"):
            message['seen_by'] = text_data_json.get("seen_by")
            message['chat_id'] = Chat.objects.get(user=self.user).pk

            if message['seen_by'] == 'admin':
                chat = Chat.objects.get(user=self.user)
                chat.admin_last_seen = timezone.now()
                chat.save(update_fields=['admin_last_seen'])
            else:
                chat = Chat.objects.get(user=self.user)
                chat.user_last_seen = timezone.now()
                chat.save(update_fields=['user_last_seen'])
                chat.save()

        # if sent data is message
        else:
            message = self.save_message(text_data_json)
            if not message:
                return

        self.send(text_data=json.dumps({"message": message}))

        # send the message to admin socket
        send_message_to_admin(message)

    def save_message(self, text_data_json):
        text = text_data_json.get('text')
        image = text_data_json.get('image')
        voice = text_data_json.get('voice')
        sent_by_admin = text_data_json.get('sent_by_admin')

        if not text and not voice and not image:
            return False

        chat_instance = Chat.objects.get(user=self.user)
        message = Message.objects.create(
            text=text,
            image=image,
            voice=voice,
            sent_by_admin=sent_by_admin,
            chat=chat_instance)

        return MessageSerializer(message).data


class AdminChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'chat'
        self.room_group_name = self.room_name+"_admin"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": 'forward_to_all',
                "message": data
            }
        )

    def forward_to_all(self, event):
        # Receive message from room group
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
