from django.db import models

from locations.models import Area


class Package(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    num_of_flights = models.SmallIntegerField()
    name = models.CharField(max_length=30)
    city = models.ForeignKey(Area, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        unique_together = ('name', 'city')



class Bus(models.Model):
    name = models.CharField(max_length=30)
    seats = models.SmallIntegerField()
    
    def __str__(self) -> str:
        return f"{self.name}({self.seats})"
    
    



class Day(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    name = models.CharField(max_length=20, choices=DAY_CHOICES, unique=True)
    
    def __str__(self):
        return f"{self.name}"


class Appointments(models.Model):
    time = models.TimeField()
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    class Meta:
        ordering = ['day', 'time']
        unique_together = ('time', 'day')


    def __str__(self):
        return f"{self.day}({self.time.strftime('%I:%M %p')})"  # This formats the time as 12-hour with AM/PM