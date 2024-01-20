from django.utils import timezone
from datetime import datetime, timedelta
import pytz

from .models import Flight, Program

def create_program(program, date):
    date = datetime.strptime(str(date), '%Y-%m-%d')
    day_name = date.strftime('%A')
    
    appointments = program.move_at.filter(day__name=day_name)
    for appoint in appointments:
        Flight.objects.get_or_create(program=program, date=date, time=appoint.time)


def create_all_programs(date):
    programs = Program.objects.all()
    for prog in programs:
        create_program(prog, date)
        
def create_all_next_30():
    date = timezone.now().date()
    
    for i in range(30):
        cur_date = date + timedelta(days=i)
        create_all_programs(cur_date)

def delete_old_flights(passed_days=1):
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date()
    deletion_date = current_date - timedelta(days=passed_days)
    # Delete old flights
    Flight.objects.filter(date__lt=deletion_date).delete()



def get_next_30_dates(start_date):
    # Convert the start_date to a datetime object
    date = datetime.strptime(start_date, '%Y-%m-%d')

    next_dates = []

    for _ in range(31):
        if date.weekday() != 4: # skip friday
            next_dates.append(date.strftime('%Y-%m-%d'))
        date += timedelta(days=1)

    return next_dates