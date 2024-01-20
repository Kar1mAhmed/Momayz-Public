from django.db import models
from users.models import User


class Chat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, unique=True)
    user_last_seen = models.DateTimeField(auto_now_add=True)
    admin_last_seen =  models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sent_by_admin = models.BooleanField()
    text = models.CharField(max_length=1000, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    voice = models.URLField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    
    
    class Meta: 
        ordering = ['time']
        
    def __str__(self) -> str:
        text = self.text if self.text is not None else "-Link-"
        sent_by = 'admin' if self.sent_by_admin else 'user'
        return f"({self.chat.user.username})-:{sent_by}--> {text}"