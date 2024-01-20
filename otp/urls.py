from django.urls import path
from .views import generate_otp, verify_otp

urlpatterns = [
    path('generate/', generate_otp),
    path('verify/', verify_otp),
]
