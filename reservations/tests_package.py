from django.test import TestCase

from reservations.models import Reservation, Subscription
from flights.models import Flight, Program
from users.models import User
from locations.models import Area, Govern
from flightsInfo.models import Bus, Appointments, Package, Day

from flights.helpers import create_all_next_30



class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.govern = Govern.objects.create(name='Test Govern')

        self.move_from_area = Area.objects.create(name='From Area', govern=self.govern)
        self.move_to_area = Area.objects.create(name='To Area', govern=self.govern)
        
        self.user = User.objects.create(email='test@example.com',
                                        name='Test User',
                                        username='testuser',
                                        gender='Male',
                                        credits=100,
                                        city=self.move_from_area)

        self.bus = Bus.objects.create(name='Test Bus', seats=10)
        
        
        self.day1 = Day.objects.create(name='Monday')
        self.day2 = Day.objects.create(name='Friday')

        self.appointment1 = Appointments.objects.create(time='12:00:00', day=self.day1)
        self.appointment2 = Appointments.objects.create(time='16:00:00', day=self.day2)


        self.program1 = Program.objects.create(govern=self.govern, move_from=self.move_from_area,
                                                move_to=self.move_to_area, bus=self.bus,price=25)
        
        self.program2 = Program.objects.create(govern=self.govern, move_from=self.move_to_area,
                                                move_to=self.move_from_area, bus=self.bus,price=25)
        
        self.program1.move_at.add(self.appointment1)
        self.program2.move_at.add(self.appointment2)
        
        self.package = Package.objects.create(price=300, num_of_flights=10, name="Test package", city=self.move_from_area)
        
        create_all_next_30()



    def test_book_package(self):
        self.user.save()
        
        package = Package.objects.get(pk=1)
        self.user.credits = package.price
        flights = Flight.objects.all()[:8]
        
    
        subscription, _ = Subscription.objects.custom_create(user=self.user, package=package, flights=flights)

        self.user.refresh_from_db()
        
        self.assertEqual(self.user.credits, 0)        
        self.assertEqual(Reservation.objects.all().count(), len(flights))
        
        for flight in flights:
            self.assertEqual(flight.taken_seats, 1)        
    

    def test_book_package_no_enough_credits(self):
        
        #Creating new instance of flights 
        Flight.objects.all().delete()
        Reservation.objects.all().delete()
        
        self.user.credits = 100
        self.user.save()
        
        package = Package.objects.get(pk=1)
        flights = Flight.objects.all()[:8]
        
        subscription, _ = Subscription.objects.custom_create(user=self.user, package=package, flights=flights)

        
        self.assertEqual(self.user.credits, 100)        
        self.assertEqual(Reservation.objects.all().count(), 0)
        
        for flight in flights:
            self.assertEqual(flight.taken_seats, 0)        
        

    
    def test_book_package_no_enough_seats(self):
        
        #Creating new instance of flights 
        Flight.objects.all().delete()
        Reservation.objects.all().delete()

        create_all_next_30()
        self.user.credits = 300
        self.user.save()
        
        package = Package.objects.get(pk=1)
        flights = Flight.objects.all()[:8]
        
        # set one flight to no seats
        full_flight = flights[7]
        full_flight.taken_seats = full_flight.total_seats
        full_flight.save()
        
        subscription, _ = Subscription.objects.custom_create(user=self.user, package=package, flights=flights)


        self.assertEqual(Reservation.objects.all().count(), 0)