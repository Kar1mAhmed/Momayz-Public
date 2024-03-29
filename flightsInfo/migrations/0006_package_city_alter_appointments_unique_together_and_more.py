# Generated by Django 4.2.6 on 2023-12-13 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_alter_area_unique_together'),
        ('flightsInfo', '0005_day_alter_appointments_options_appointments_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='locations.area'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='appointments',
            unique_together={('time', 'day')},
        ),
        migrations.AlterUniqueTogether(
            name='package',
            unique_together={('name', 'city')},
        ),
    ]
