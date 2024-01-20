from django.urls import path
from .views import get_packages, return_appointments, go_appointments

urlpatterns = [
    path('packages/', get_packages),
    path('go-at/', go_appointments),
    path('return-at/', return_appointments)
]
