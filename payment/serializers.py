from .models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    success = serializers.SerializerMethodField()
    transaction_id = serializers.SerializerMethodField()
    class Meta:
        model = Payment
        fields = ['transaction_id', 'amount_cents',  'success', 'created_at', 'created_at','payment_type']
        
    def get_success(self, obj):
        return str(obj.success)
    
    def get_transaction_id(self, obj):
        return  str(obj.transaction_id)