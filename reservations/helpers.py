from flights.models import Flight, Program
from .models import Reservation

from django.utils import timezone
from datetime import datetime, timedelta
import pytz


def delete_old_reservations(passed_days=1):
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date()
    deletion_date = current_date - timedelta(days=passed_days)

    # Delete old flights
    Reservation.objects.filter(flight__date__lt=deletion_date).delete()





def get_flights(days, user):
    '''
        the idea to get the flights of the days user picked and reserve it for 4 weeks ahead.
    '''
    flights = []
    for day in days:
        dates_of_day = get_dates(day['day'])
        for date in dates_of_day:
            # The Flight that goes from user Home to Collage
            try :
                flights.append(Flight.objects.get(date=date, program__move_from=user.city, time=day['go_at']))
                # The Flight that goes from Collage to user destination 
                flights.append(Flight.objects.get(date=date, program__move_to=user.city, time=day['return_at']))
            except Exception as _:
                return False
    return flights


def get_dates(base_dates):
    dates_to_reserve = []
    dates_to_reserve.append(base_dates) # append the base date
    for num_of_weeks in range(1,4): # To reserve the same day after 1,2,3 weeks
        dates_to_reserve.append(date_after_num_of_weeks(base_dates, num_of_weeks))
    return dates_to_reserve


def date_after_num_of_weeks(date, num_weeks):
    # Convert the given date to a datetime object
    date_format = '%Y-%m-%d'
    given_date_datetime = datetime.strptime(date, date_format)

    # Calculate the date one week (7 days) after the given date
    days= num_weeks * 7
    one_week_after = given_date_datetime + timedelta(days=days)

    # Format the result as 'YYYY-MM-DD' again
    one_week_after_formatted = one_week_after.strftime(date_format)
    return one_week_after_formatted