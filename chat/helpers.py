from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

import base64
import json
from asgiref.sync import async_to_sync


from channels.layers import get_channel_layer


def send_message_to_admin(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_admin',
        {
            'type': 'forward_to_all',
            'message': data
        }
    ) 


def get_user_from_token(token):
        try:
            payload = json.loads(base64.b64decode(token.split('.')[1] + '==').decode('utf-8'))
            user_id = payload.get('user_id')
            return get_user_model().objects.get(username=user_id)
        except (Token.DoesNotExist, User.DoesNotExist, KeyError, json.JSONDecodeError):
            return None

def get_token_from_headers(headers):
        # Search for the "authorization" header within the list of headers
        for key, value in headers:
            if key == b'authorization':
                return value.decode('utf-8')
    
    
def get_user(headers):
        authorization_header = get_token_from_headers(headers)
        
        if authorization_header:
            token = authorization_header  # The token is the authorization header
            user = get_user_from_token(token)
            if user:
                return user
        return None