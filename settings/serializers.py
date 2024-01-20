from .models import QA
from rest_framework import serializers


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = '__all__'

