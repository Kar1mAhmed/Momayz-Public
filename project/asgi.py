import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django_asgi_app = get_asgi_application()


from channels.auth import AuthMiddlewareStack
    

from channels.security.websocket import AllowedHostsOriginValidator 
import chat.routing


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(  # new
        AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)))
})