# Generated by Django 4.2.6 on 2023-10-09 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flightsInfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointments',
            options={'ordering': ['time']},
        ),
    ]
