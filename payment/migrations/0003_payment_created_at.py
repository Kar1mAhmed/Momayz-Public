# Generated by Django 4.2.6 on 2023-11-22 03:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_payment_id_payment_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
