from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'city', 'govern', 'credits']
    search_fields = ['username', 'name'] 
    list_filter = ['city', 'city__govern']
    exclude = ['password', 'img', 'notification_token', 'is_active']
    # readonly_fields = ['username', 'name', 'email', 'gender', 'city']



    
    def govern(self, obj):
        if obj.city:
            return obj.city.govern
        return None
    


admin.site.register(User, UserAdmin)