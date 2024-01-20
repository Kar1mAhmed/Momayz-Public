from django.urls import path, include

from .views import *

urlpatterns = [
    path('<str:pk>', UserDetails.as_view()),
    path('logout/', CustomLogoutView.as_view()),
    path('login/', CustomLoginView.as_view()),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('rest-password/', reset_password)
]
