from django.urls import path
from .views import AreaView, GovernView

urlpatterns = [
    path('govern/', GovernView.as_view()),
    path('city/', AreaView.as_view()),
]
