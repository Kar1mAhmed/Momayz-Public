from rest_framework import serializers
from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        
        
class ChatSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name')
    last_message = serializers.SerializerMethodField()
    unread_admin = serializers.SerializerMethodField()
    unread_user = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = '__all__'
        
    def get_last_message(self, obj):
        last_message = Message.objects.filter(chat=obj).last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def get_unread_admin(self, obj):
        last_message = Message.objects.filter(chat=obj, sent_by_admin=False).last()
        
        if last_message and last_message.time > obj.admin_last_seen:
            return True
        return False
    
    def get_unread_user(self, obj):
        last_message = Message.objects.filter(chat=obj, sent_by_admin=True).last()
        
        if last_message and last_message.time > obj.user_last_seen:
            return True
        return False
