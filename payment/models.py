from django.db import models

from users.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.IntegerField()
    order_id = models.IntegerField()
    amount_cents = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    currency = models.CharField(max_length=20)
    pending = models.BooleanField()
    success = models.BooleanField()
    created_at = models.DateTimeField()
    payment_type = models.CharField(max_length=20)
