# Generated by Django 4.2.6 on 2023-10-05 08:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 5, 11, 13, 30, 684618)),
        ),
    ]
