from rest_framework import serializers
from .models import Flight
from datetime import datetime


class FlightSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='program.move_from')
    move_to = serializers.CharField(source='program.move_to')
    price = serializers.CharField(source='program.price')
    flight_type = serializers.SerializerMethodField()
    arrive_at = serializers.SerializerMethodField()
    class Meta:
        model = Flight
        fields = ['id', 'date', 'time', 'taken_seats', 'total_seats',
                    'move_from', 'move_to', 'price', 'flight_type', 'arrive_at']

    def get_flight_type(self, obj):
        move_to = obj.program.move_to
        
        if move_to.name == 'الجامعة':
            return 'ذهاب'
        else:
            return 'عودة'
        
    def get_arrive_at(self, obj):
        time_as_datetime = datetime.combine(datetime.min, obj.time)
        return (time_as_datetime + obj.program.duration).time()

