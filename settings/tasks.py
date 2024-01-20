from celery import shared_task

from flights.helpers import delete_old_flights, create_all_programs
from reservations.helpers import delete_old_reservations

from django.utils import timezone

from datetime import  timedelta, datetime
import pytz

from .helpers import *
from otp.helpers import delete_old_otps

from flights.models import Flight

@shared_task(bind=True)
def midnight(self, reservation_days=30, flights_days=30):
    delete_old_reservations(reservation_days)
    delete_old_flights(flights_days)
    delete_old_otps()
    cairo_timezone = pytz.timezone('Africa/Cairo')
    today_date = timezone.now().astimezone(cairo_timezone).date()
    date_after_30 = today_date + timedelta(days=30)
    
    create_all_programs(date_after_30)



@shared_task(bind=True)
def flight_notification(self):
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_datetime = timezone.now().astimezone(cairo_timezone)
    Flights = Flight.objects.filter(date=current_datetime.today(), notified=False)

    time_in_30m =(datetime.combine(current_datetime.today(), current_datetime.time()) + timedelta(minutes=32)).time()

    for flight in Flights:
        if flight.time < time_in_30m:
            notify_flight(flight.pk)
            flight.notified = True
            flight.save()