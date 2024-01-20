from django.contrib import admin

from .models import Reservation, Subscription
from django.utils import timezone
import pytz


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ['seat_number', 'subscription']
    list_display = ['user_name', 'user_username', 'flight_move_from',
                    'flight_move_to', 'flight_date', 'flight_time']
    search_fields = ["flight__program__move_from__name", "flight__program__move_to__name", "flight__date", "flight__time"] 
    list_filter = ["flight__program__move_from", "flight__program__move_to",  "flight__time", 'flight__date', 'flight__program__price']
    autocomplete_fields = ('user',)


    actions = ['immediate_delete']

    def immediate_delete(self, request, queryset):
        for item in queryset:
            item.delete()
        self.message_user(
            request,
            f"items deleted.",
        )

    immediate_delete.short_description = "Delete selected items "
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        cairo_timezone = pytz.timezone('Africa/Cairo')
        current_date = timezone.now().astimezone(cairo_timezone).date()
        return qs.filter(flight__date__gte=current_date)
    
    def get_actions(self, request):
        # Override the get_actions method to exclude the delete action
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions
    
    def user_name(self, obj):
        return obj.user.name
    
    user_name.short_description = 'User Name'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User Phone'

    def flight_move_from(self, obj):
        return obj.flight.program.move_from
    flight_move_from.short_description = 'Move From'

    def flight_move_to(self, obj):
        return obj.flight.program.move_to
    flight_move_to.short_description = 'Move To'

    def flight_date(self, obj):
        return obj.flight.date
    flight_date.short_description = 'Date'

    def flight_time(self, obj):
        return obj.flight.time
    flight_time.short_description = 'Time'
    
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'passed_flights', 'total_flights']
    
    
    actions = ['immediate_delete']
    
    
    def get_actions(self, request):
        # Override the get_actions method to exclude the delete action
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def immediate_delete(self, request, queryset):
        for item in queryset:
            item.delete()
        self.message_user(
            request,
            f"items deleted.",
        )

    immediate_delete.short_description = "Delete selected items"
    
    def total_flights(self, obj):
        return obj.total_flights_count()
    total_flights.short_description = 'total_flights'
    
    def passed_flights(self, obj):
        return obj.passed_flights_count()
    passed_flights.short_description = 'passed_flights'

    
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Subscription, SubscriptionAdmin)