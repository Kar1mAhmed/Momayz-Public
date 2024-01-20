from django.contrib import admin
from .models import Govern, Area
# Register your models here.

class GovernAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Govern._meta.fields]

admin.site.register(Govern, GovernAdmin)


class AreaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Area._meta.fields]
    
admin.site.register(Area, AreaAdmin)
