# Generated by Django 4.2.6 on 2023-11-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0019_flight_notified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='duration',
            field=models.DurationField(default='00:00:00'),
        ),
    ]
