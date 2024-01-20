from django.contrib import admin
from .models import OTP
# Register your models here.

class OTPAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OTP._meta.fields]


# admin.site.register(OTP, OTPAdmin)