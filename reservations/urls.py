from django.urls import path
from .views import  ReservationView, PackageView, edit_reservation

urlpatterns = [
    path('', ReservationView.as_view()),
    path('edit/', edit_reservation),
    path('package/', PackageView.as_view()),
]
