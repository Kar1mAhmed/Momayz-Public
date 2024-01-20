from rest_framework import serializers
from .models import Reservation, Subscription

from datetime import datetime


class ReservationSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='flight.program.move_from')
    move_to = serializers.CharField(source='flight.program.move_to')
    date = serializers.CharField(source='flight.date')
    price = serializers.CharField(source='flight.program.price')
    time = serializers.CharField(source='flight.time')
    arrive_at = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        exclude = ['reserved_at', 'user', 'flight']
        
    def get_arrive_at(self, obj):
        time_as_datetime = datetime.combine(datetime.min, obj.flight.time)
        return (time_as_datetime + obj.flight.program.duration).time()


class SubscriptionSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name')
    total_reservations = serializers.CharField(source='package.num_of_flights')
    price = serializers.CharField(source='package.price')
    passed_reservations = serializers.SerializerMethodField()
    class Meta:
        model = Subscription
        exclude = ['package', 'user', 'id', 'reservations']
        
    def get_passed_reservations(self, obj):
        return obj.passed_flights_count()