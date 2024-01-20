from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from project.settings import HMAC_KEY

from .serializers import PaymentSerializer

from users.models import User
from .models import Payment

import hashlib
import hmac

class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        if not self.HMAC_authentication(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
    
        user_phone = request.data['obj']['payment_key_claims']['billing_data']['phone_number']
        user = User.objects.get(username=user_phone)
        
        success = request.data['obj']['success']
        payment = self.save_transaction(request, user)

        if success:
            amount = request.data['obj']['data']['amount'] / 100
            user.refund_credits(int(amount))
            user.send_notification(f'تم إضافة {amount} جنية لحسابكم.', details=payment) 
            return Response(payment, status=status.HTTP_200_OK)

        user.send_notification(f'حدث خطأ أثناء شحن الرصيد.', details=payment) 
        return Response(payment, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)




    def save_transaction(self, request, user):
        currency = request.data['obj']['currency']
        order_id = request.data['obj']['order']['id']
        created_at = request.data['obj']['created_at']
        pending = request.data['obj']['pending']
        success = request.data['obj']['success']
        amount_cents = request.data['obj']['amount_cents']
        transaction_id = request.data['obj']['id']
        payment_type = request.data['obj']['source_data']['type']
        
        payment = Payment.objects.create(
            currency=currency,
            order_id=order_id,
            created_at=created_at,
            pending=pending,
            success=success,
            amount_cents=amount_cents,
            transaction_id=transaction_id,
            payment_type=payment_type,
            user=user
            )
        return PaymentSerializer(payment).data

    def HMAC_authentication(self, request):
        values = [
            str(request.data['obj']['amount_cents']),
            request.data['obj']['created_at'],
            request.data['obj']['currency'],
            str(request.data['obj']['error_occured']).lower(),
            str(request.data['obj']['has_parent_transaction']).lower(),
            str(request.data['obj']['id']),
            str(request.data['obj']['integration_id']),
            str(request.data['obj']['is_3d_secure']).lower(),
            str(request.data['obj']['is_auth']).lower(),
            str(request.data['obj']['is_capture']).lower(),
            str(request.data['obj']['is_refunded']).lower(),
            str(request.data['obj']['is_standalone_payment']).lower(),
            str(request.data['obj']['is_voided']).lower(),
            str(request.data['obj']['order']['id']),
            str(request.data['obj']['owner']),
            str(request.data['obj']['pending']).lower(),
            str(request.data['obj']['source_data']['pan']),
            str(request.data['obj']['source_data']['sub_type']),
            str(request.data['obj']['source_data']['type']),
            str(request.data['obj']['success']).lower()]
            
        
        concatenated_string  = ''.join(values)

        hashed_message = hmac.new(
        key=HMAC_KEY.encode('utf-8'),
        msg=concatenated_string.encode('utf-8'),
        digestmod=hashlib.sha512).hexdigest()
        
        received_hash = request.GET.get('hmac')

        
        if hashed_message == received_hash:
            return True
        
        return False
