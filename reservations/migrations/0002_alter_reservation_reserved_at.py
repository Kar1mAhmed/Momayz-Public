# Generated by Django 4.2.6 on 2023-10-14 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reserved_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
