from django.test import TestCase
from reservations.models import Reservation
from flights.models import Flight, Program
from users.models import User
from locations.models import Area, Govern
from flightsInfo.models import Bus, Appointments, Day


class ReservationModelTestCase(TestCase):
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

    def test_create_reservation(self):
        # Save the initial values
        initial_taken_seats = self.flight.taken_seats
        initial_user_credits = self.user.credits
        
        reservation = Reservation.objects.create(user=self.user, flight=self.flight)
        next_expected_seat_number = reservation._get_seat_number(reservation.flight, self.user.gender)
        last_seat_number = next_expected_seat_number + 1

        # Retrieve the flight and user instances again to get updated values
        self.flight.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(self.flight.taken_seats, initial_taken_seats + 1)
        self.assertEqual(self.user.credits, initial_user_credits - self.flight.program.price)

        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.flight, self.flight)
        self.assertEqual(reservation.seat_number, last_seat_number)
        
    def test_replace_reservation(self):
        
        flight1 = Flight.objects.create(program=self.program1, date='2023-10-29')
        flight2 = Flight.objects.create(program=self.program1, date='2023-10-30')

        flight1.taken_seats = 5
        flight2.taken_seats = 8
        flight1.save()
        flight2.save()

        initial_user_credits = self.user.credits
        
        reservation = Reservation.objects.create(user=self.user, flight=flight1)
        self.assertEqual(flight1.taken_seats, 6)
        
        reservation.replace(flight2.pk)
        
        flight1.refresh_from_db()
        flight2.refresh_from_db()
        self.user.refresh_from_db()
        
        self.assertEqual(flight1.taken_seats, 5)
        self.assertEqual(flight2.taken_seats, 9)
        self.assertEqual(initial_user_credits, self.user.credits + flight2.program.price)

        self.assertEqual(reservation.flight.date, flight2.date)

    def test_no_enough_seats(self):
    
        flight = Flight.objects.create(program=self.program1, date='2023-10-29')
        flight.taken_seats = flight.program.bus.seats
        flight.save()
        
        user_init_credits = self.user.credits
        flight_init_seats = flight.taken_seats
        
        with self.assertRaises(ValueError):
            reservation = Reservation.objects.create(user=self.user, flight=flight)
            
        self.assertEqual(user_init_credits, self.user.credits)
        self.assertEqual(flight_init_seats, flight.taken_seats)
    
    def test_no_enough_credits(self):
        flight = Flight.objects.create(program=self.program1, date='2023-10-29')
        
        self.user.credits = 20
        self.user.save()
        
        self.user.refresh_from_db()

        
        with self.assertRaises(ValueError):
            reservation = Reservation.objects.create(user=self.user, flight=flight)
            
        self.assertEqual(self.user.credits, 20)
    
    def test_replace_no_seats(self):
        self.user.credits = 100
        self.user.save()
        
        flight1 = Flight.objects.create(program=self.program1, date='2023-10-30')
        
        flight2 = Flight.objects.create(program=self.program1, date='2023-10-29')
        flight2.taken_seats = flight2.program.bus.seats
        flight2.save()
        
        init_f1_seats = flight1.taken_seats
        init_f2_seats = flight2.taken_seats
        init_user_credits = self.user.credits
        
        reservation = Reservation.objects.create(user=self.user, flight=flight1)
        
        with self.assertRaises(ValueError):
            reservation.replace(flight2.pk)
            
        self.user.refresh_from_db()
        flight1.refresh_from_db()
        flight2.refresh_from_db()

        self.assertEqual(init_f1_seats + 1, flight1.taken_seats)
        self.assertEqual(init_f2_seats, flight2.taken_seats)
        self.assertEqual(init_user_credits, self.user.credits + flight1.program.price)

    def test_replace_diff_destinations(self):
        
        program2 = Program.objects.create(govern=self.govern, move_from=self.move_from_area,
                                                move_to=self.move_from_area, bus=self.bus,price=150)
        program2.move_at.add(self.appointment)
        
        flight1 = Flight.objects.create(program=self.program1, date='2023-10-30')
        flight2 = Flight.objects.create(program=program2, date='2023-10-29')
        
        init_f1_seats = flight1.taken_seats
        init_f2_seats = flight2.taken_seats
        init_user_credits = self.user.credits
        
        reservation = Reservation.objects.create(user=self.user, flight=flight1)
        
        
        with self.assertRaises(ValueError):
            reservation.replace(flight2.pk)
        
        
        self.user.refresh_from_db()
        flight1.refresh_from_db()
        flight2.refresh_from_db()

        self.assertEqual(init_f1_seats + 1, flight1.taken_seats)
        self.assertEqual(init_f2_seats, flight2.taken_seats)
        self.assertEqual(init_user_credits, self.user.credits + flight1.program.price)
    
    def test_no_seat_number_conflict(self):
        # Create a flight with enough seats
        flight = Flight.objects.create(program=self.program1, date='2023-10-29', total_seats=50)  # Adjust seat numbers as needed

        # Create a user
        user = User.objects.create(email='testo@example.com', name='Test User', username='testuser2', gender='Male', credits=5000)

        seat_numbers = []
        num_reservations = 15

        for _ in range(num_reservations):
            reservation = Reservation.objects.create(user=user, flight=flight)

        # Delete some of the reservations (e.g., every even seat number reservation)
        reservations_to_delete = Reservation.objects.filter(seat_number__in=range(2, num_reservations, 2))
        reservations_to_delete.delete()
        
        for i in range(3):
            reservation = Reservation.objects.create(user=user, flight=flight)

        flight_seats_taken = Reservation.objects.filter(flight=flight).values_list('seat_number', flat=True)
        

        self.assertEqual(list(flight_seats_taken), list(set(flight_seats_taken)))

    def test_check_seat_number(self):
        program_local = Program.objects.create(govern=self.govern, move_from=self.move_from_area,
                                                move_to=self.move_from_area, bus=self.bus,price=50)
        program_local.move_at.add(self.appointment)
        flight = Flight.objects.create(program=program_local, date='2023-10-11')
        
        user = User.objects.create(email='teto@example.com', name='M User',
                                    username='Medo12', gender='Female', credits=250)
        
        reservations = []
        for i in range(1,6):
            res =Reservation.objects.create(flight=flight, user=user)
            reservations.append(res)
            
        reservations[1].delete()
        
        new_reservation = Reservation.objects.create(flight=flight, user=user)
        
        user.refresh_from_db()
        
        self.assertEqual(user.credits, 0)
        self.assertEqual(new_reservation.seat_number, 2)

    def test_gender_seats(self):
        flight = Flight.objects.create(program=self.program1, date='2012-12-12')
        
        for i in range(5):
            female = User.objects.create(email=f'{i}@example.com', name=f'UserFemale{i}',
                                        username=f'FemaleUser{i}', gender='Female', credits=100)
            res = Reservation.objects.create(user=female, flight=flight)
            self.assertLess(res.seat_number, 6)
            
        for i in range(5):
            female = User.objects.create(email=f'{i*2}@Male.com', name=f'UserMale{i*2}',
                                        username=f'MaleUser{i*2}', gender='Male', credits=100)
            res = Reservation.objects.create(user=female, flight=flight)
            self.assertGreater(res.seat_number, 5)
