# Generated by Django 4.2.6 on 2023-10-20 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0014_rename_cancelled_flight_canceled'),
        ('reservations', '0003_alter_reservation_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('flight', 'seat_number')},
        ),
    ]
