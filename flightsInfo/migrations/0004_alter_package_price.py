# Generated by Django 4.2.6 on 2023-10-24 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightsInfo', '0003_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
