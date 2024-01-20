from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist

from dj_rest_auth.views import LogoutView, LoginView

from .models import User
from .serializers import *

from otp.models import OTP

class UserDetails(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserDetailsSerializer


class CustomLogoutView(LogoutView):
     def post(self, request, *args, **kwargs):
        try:
            request.user.remove_notification_token()
        except Exception:
            pass
        return self.logout(request)


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        
        # Update notification token if it's in the request body
        if 'notification_token' in request.data:
            notfy_token = request.data['notification_token']
            response = self.get_response()
            
            # if user authorized successfully 
            if 'access' in response.data:
                request.user.update_notification_token(notfy_token)
                response.data['user']['notification_token'] = notfy_token
                
            return response
        
        return self.get_response()



@api_view(['POST'])
def reset_password(request):
    phone_number = request.data['username']
    pass1= request.data['password']
    pass2= request.data['password2']
    otp= request.data['otp']
    
    if pass1 == pass2:
        otp_status = get_otp_status(phone_number, otp)
        if otp_status == "good" :
            try:
                user = User.objects.get(username=phone_number)
            except ObjectDoesNotExist:
                return Response({'detail': "No user with this phone number"}, status=status.HTTP_404_NOT_FOUND)

            user.set_password(pass1)
            user.save()
            return Response({'detail': "Password reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': otp_status}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail' : "Password Doesn't match."}, status=status.HTTP_401_UNAUTHORIZED)
    
    
def get_otp_status(phone_number, otp):
    last_otp = OTP.objects.filter(phone_number=phone_number).order_by('-created_at').first()
    if not last_otp:
        return "No OTP for this number"
    if last_otp.code != otp :
        return "Wrong OTP."
    if last_otp.is_expired():
        return "OTP expired."
    return "good"