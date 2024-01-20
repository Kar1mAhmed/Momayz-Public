from django.db import models

from locations.models import Area, Govern
from flightsInfo.models import Appointments, Bus

from django.core.validators import MinValueValidator

from datetime import timedelta


class Program(models.Model):
    govern = models.ForeignKey(Govern, on_delete=models.PROTECT, default=1)
    move_from = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="move_from")
    move_to = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="move_to")
    move_at = models.ManyToManyField(Appointments)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    duration = models.DurationField(default=timedelta(minutes=30))
    price = models.DecimalField(max_digits=8, decimal_places=2)
    auto_create = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('move_from', 'move_to')
    
    def __str__(self) -> str:
        return f"{self.move_from} إلي {self.move_to}"




class Flight(models.Model):
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField(default="00:00:00")
    taken_seats = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    total_seats = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    notified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('time', 'program', 'date')
        ordering = ['date', 'time']

    def __str__(self) -> str:
        return f"{self.program.move_from} إلي {self.program.move_to} ({self.date} | {self.time})"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if str(self.time) == '00:00:00':
                self.time = self.program.move_at.first().time
            if not self.total_seats:
                self.total_seats = self.program.bus.seats
            
        super().save(*args, **kwargs)


    def increment_taken_seats(self):
        Flight.objects.select_for_update().get(pk=self.pk)
        if self.taken_seats < self.total_seats:
            self.taken_seats += 1
            self.save()
        else:
            raise ValueError("Seats reaching limits.")
        
    def decrement_taken_seats(self):
        if self.taken_seats > 0:
            self.taken_seats -= 1
            self.save()
        else:
            raise ValueError("Seats reaching limits.")

    def is_full(self):
        return (self.taken_seats >= self.total_seats)
