from .models import Govern, Area
from rest_framework import serializers


class GovernSerializer(serializers.ModelSerializer):
    class Meta:
        model = Govern
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'