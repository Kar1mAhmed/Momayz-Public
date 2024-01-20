from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Message, Chat
from .serializers import MessageSerializer, ChatSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_chat(request):
    user = request.user
    chat, created = Chat.objects.get_or_create(user=user)
    messages = Message.objects.filter(chat=chat)
    serialized_data = MessageSerializer(messages, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def chat_list(request):
    chats = Chat.objects.all()

    # Exclude chats without a last message
    chats_with_last_message = [chat for chat in chats if Message.objects.filter(chat=chat).exists()]

    serialized_data = ChatSerializer(chats_with_last_message, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)