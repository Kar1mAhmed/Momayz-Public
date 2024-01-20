from django.db import models, transaction

from users.models import User
from flights.models import Flight
from flightsInfo.models import Package

from django.utils import timezone
import pytz



class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING, db_index=True)
    reserved_at = models.DateTimeField(auto_now_add=True)
    seat_number = models.SmallIntegerField()
    subscription = models.ForeignKey('Subscription', related_name='subscription', on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)

    
    class Meta:
        ordering = ['flight__date', 'flight__time']
        unique_together = ('flight', 'seat_number')

    def __str__(self) -> str:
        return f'reservation of {self.user.name} for flight ({self.flight.program.move_from} to {self.flight.program.move_to}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                seat_number = self._get_seat_number(self.flight, self.user.gender)
                if seat_number:
                    if self._handel_credits():
                        self.seat_number = seat_number
                        self.flight.increment_taken_seats()
                        return super().save(*args, **kwargs)
                    else:
                        raise ValueError("No enough credits.")
                else:
                    raise ValueError("Flight is full.")
        return super().save(*args, **kwargs)
        
    
    def delete(self, refund=True, *args, **kwargs):
        try:
            with transaction.atomic():
                self.flight.decrement_taken_seats()
                if refund:
                    if self.subscription :
                        credits_to_refund = self.subscription.package.price / self.subscription.package.num_of_flights
                        self.user.refund_credits(credits_to_refund)
                    else:
                        credits_to_refund = self.flight.program.price
                        self.user.refund_credits(self.flight.program.price)
                return super().delete(*args, **kwargs)
        except Exception as e:
            raise e
    
    
    def replace(self, flight_to_reserve_id):
        flight_to_reserve = Flight.objects.get(pk=flight_to_reserve_id)
        
        
        if flight_to_reserve.taken_seats >= flight_to_reserve.total_seats:
            raise ValueError('No enough seats')
        
        if flight_to_reserve.program.move_from != self.flight.program.move_from \
            or flight_to_reserve.program.move_to != self.flight.program.move_to:
                raise ValueError('The flight should have the same destinations.')
        
        try:
            with transaction.atomic():
                self.flight.decrement_taken_seats()
                flight_to_reserve.increment_taken_seats()
                
                seat = self._get_seat_number(flight_to_reserve, self.user.gender)
                
                self.flight = flight_to_reserve
                self.seat_number = seat
                self.save()
                return self
                
        except Exception as e:
            raise str(e)
        
    def _get_seat_number(self, flight, gender): 
        '''
        this is the most safe way to get seat number by spreading man's from women's.
        
        reserved_seat_numbers should be listed because reservation could be cancelled
        so some in middle seats could be empty, keeping track of all reserved seats
        will be inefficient in terms of storage and will cause some critical section problems,
        and listing the seats in every reservation will be overhead but it will be safer.
        '''

        flight_instance = Flight.objects.select_for_update().get(pk=flight.pk)
        if flight.taken_seats >= flight.total_seats:
                return None

        reserved_seat_numbers = set(Reservation.objects.filter(flight=flight) \
                                        .values_list('seat_number', flat=True))
            
            # separate males from females
        if gender == 'Female': 
            start = 1
            end = flight.total_seats + 1
            move = 1
        else:
            start = flight.total_seats 
            end = 0
            move = -1
                
        for seat_number in range(start, end, move):
                if seat_number not in reserved_seat_numbers:
                    return seat_number
        return None
        
        
    def _handel_credits(self):
        if not self.subscription:
            try:
                self.user.deduct_credits(self.flight.program.price)
                return True
            except:
                return False
        return True




class SubscriptionManager(models.Manager):
    def custom_create(self, package, user, flights):
        try:
            # Create a subscription
            with transaction.atomic():
                subscription = self.create(package=package, user=user)
                # Create reservations and set first_flight_date and last_flight_date
                reservations = []
                last_flight = None
                for flight in flights:
                    last_flight = flight
                    reservation = Reservation.objects.create(user=user, flight=flight, subscription=subscription)
                    reservations.append(reservation)
                subscription.reservations.set(reservations)
            
                subscription.user.deduct_credits(subscription.package.price)
                subscription.collect_flights_info()
        except Exception as e:
            return False, last_flight

        return True, subscription




class Subscription(models.Model):
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    first_flight_date = models.DateField(null=True, blank=True)
    last_flight_date = models.DateField(null=True, blank=True)
    reservations= models.ManyToManyField(Reservation, related_name='reservations')
    
    objects = SubscriptionManager()
    
    
    def __str__(self) -> str:
        return f'{self.package.name} of {self.user.name}'
    
    def delete(self, *args, **kwargs):
        for res in self.reservations.all():
            res.delete()
            
        return super().delete(*args, **kwargs)

    def collect_flights_info(self):
        first_date = None
        last_date = None
        
        for res in self.reservations.all():
            if first_date is None or first_date > res.flight.date:
                first_date = res.flight.date
            if last_date is None or last_date < res.flight.date:
                last_date = res.flight.date

        self.first_flight_date = first_date
        self.last_flight_date = last_date
        self.save()
            
            
    def remaining_flights_count(self):
        cairo_timezone = pytz.timezone('Africa/Cairo')
        today = timezone.now().astimezone(cairo_timezone).date()
        current_time = timezone.now().astimezone(cairo_timezone).time()

        remaining_reservations = self.reservations.filter(
                                        models.Q(flight__date__gt=today) | 
                                        (models.Q(flight__date=today) & 
                                        models.Q(flight__time__gt=current_time)))
        return remaining_reservations.count()
    
    def passed_flights_count(self):
        return self.package.num_of_flights - self.remaining_flights_count()
    
    def total_flights_count(self):
        return self.package.num_of_flights