from reservations.models import Reservation
from flights.models import Flight
from users.models import User

def notify_flight(flight_id):
    flight_reservations = Reservation.objects.filter(flight=flight_id)
    unique_users = User.objects.filter(id__in=flight_reservations.values('user').distinct())
    
    flight = Flight.objects.get(pk=flight_id)
    notification_body = f'ستنطلق رحلتك من {flight.program.move_from} إلي {flight.program.move_to} قريبا.'
    
    for user in unique_users:
        user.send_notification(notification_body)





    # # Check the response
    # if response.status_code == 200:
    #     print("Notification sent successfully.")
    # else:
    #     print("Failed to send notification. Status code:", response.status_code)
    #     print("Response content:", response.content)
        
        
