from django.test import TestCase
from reservations.models import Reservation
from flights.models import Flight, Program
from users.models import User
from locations.models import Area, Govern
from flightsInfo.models import Bus, Appointments, Day


class FlightModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User', username='testuser', gender='Male', credits=100)
        self.govern = Govern.objects.create(name='Test Govern')

        self.move_from_area = Area.objects.create(name='From Area', govern=self.govern)
        self.move_to_area = Area.objects.create(name='To Area', govern=self.govern)

        self.bus = Bus.objects.create(name='Test Bus', seats=10)
        
        self.day1 = Day.objects.create(name='Monday')
        self.appointment = Appointments.objects.create(time='12:00:00', day=self.day1)

        self.program1 = Program.objects.create(govern=self.govern, move_from=self.move_from_area,
                                                move_to=self.move_to_area, bus=self.bus, price=50)
        
        self.program1.move_at.add(self.appointment)
        self.flight = Flight.objects.create(program=self.program1, date='2023-10-20')
        
    
    def test_increment_taken_seats(self):
        self.flight.taken_seats = self.flight.total_seats - 1
        current_taken_seats = self.flight.taken_seats
        self.flight.increment_taken_seats()
        
        self.assertEqual(self.flight.taken_seats, current_taken_seats+1)
    
    def test_increment_taken_seats_full(self):
        self.flight.taken_seats = self.flight.total_seats
        self.flight.save()
        self.flight.refresh_from_db()       
        with self.assertRaises(ValueError):
            self.flight.increment_taken_seats()
    
    
    def test_decrement_taken_seats(self):
        self.flight.taken_seats = 1
        current_taken_seats = self.flight.taken_seats
        self.flight.decrement_taken_seats()
        self.flight.refresh_from_db()        

        self.assertEqual(current_taken_seats - 1, self.flight.taken_seats)
    
    def test_decrement_taken_seats_empty(self):
        self.flight.taken_seats = 0
        self.flight.refresh_from_db()        
        with self.assertRaises(ValueError):
            self.flight.decrement_taken_seats()
    
    def test_flight_is_full(self):
        self.flight.taken_seats = self.flight.total_seats
        self.assertTrue(self.flight.is_full())
    
    def test_flight_not_full(self):
        self.flight.taken_seats = self.flight.total_seats - 1
        self.flight.save()
        self.flight.refresh_from_db()
        
        self.assertFalse(self.flight.is_full())