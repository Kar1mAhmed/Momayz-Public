from rest_framework import serializers
from .models import Package, Appointments

class PackageSerializer(serializers.ModelSerializer):
    # days_per_week = serializers.SerializerMethodField()
    class Meta:
        model = Package
        exclude = ['city']

    # def get_days_per_week(self, obj):
    #     return int(obj.num_of_flights / 4)


class AppointmentsSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='day.name')
    class Meta:
        model = Appointments
        fields = ['time', 'day_name']
