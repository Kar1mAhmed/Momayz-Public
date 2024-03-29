# Generated by Django 4.2.6 on 2023-10-10 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_alter_area_unique_together'),
        ('flights', '0009_alter_flight_available_seats_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='govern',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='locations.govern'),
        ),
    ]
