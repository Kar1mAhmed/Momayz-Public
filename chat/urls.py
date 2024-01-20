from django.urls import path
from .views import get_chat, chat_list


urlpatterns = [
    path('', get_chat),
    path('list/', chat_list),
]
