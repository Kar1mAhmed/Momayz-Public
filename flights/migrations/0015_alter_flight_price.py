# Generated by Django 4.2.6 on 2023-10-21 15:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0014_rename_cancelled_flight_canceled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='price',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
