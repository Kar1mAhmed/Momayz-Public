from django.db import models
from django.utils import timezone


class OTP(models.Model):
    phone_number = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6)
    
    OTP_EXPIRATION_MIN = 15

    def is_expired(self):
        current_time = timezone.now()
        time_difference = current_time - self.created_at
        return time_difference.total_seconds() >= self.OTP_EXPIRATION_MIN * 60
