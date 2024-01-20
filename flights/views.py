from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.db import models
from django.db.models import Q
from django.utils import timezone


from datetime import  timedelta
import pytz


from .models import Flight
from .serializers import FlightSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_flights(request):
    user = request.user 
    city = user.city
    
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date()
    
    
    flights = Flight.objects.filter(
    Q(program__move_from=city) | Q(program__move_to=city), 
    taken_seats__lt=models.F('total_seats'),
    date=current_date
    )

    data_serialized = FlightSerializer(flights, many=True)
    return Response(data_serialized.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tomorrow_flights(request):
    user = request.user 
    city = user.city
    
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date() + timedelta(days=1)

    flights = Flight.objects.filter(
    Q(program__move_from=city) | Q(program__move_to=city), 
    taken_seats__lt=models.F('total_seats'),
    date=current_date,
    )

    data_serialized = FlightSerializer(flights, many=True)
    return Response(data_serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def flights_by_date(request):
    
    date = request.GET.get('date')
    move_from = request.GET.get('move_from')
    move_to = request.GET.get('move_to')

    flights = Flight.objects.filter(
    program__move_from__name=move_from,
    program__move_to__name=move_to, 
    taken_seats__lt=models.F('total_seats'),
    date=date,
    )

    data_serialized = FlightSerializer(flights, many=True)
    return Response(data_serialized.data, status=status.HTTP_200_OK)
