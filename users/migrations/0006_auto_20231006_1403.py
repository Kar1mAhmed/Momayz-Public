# Generated by Django 3.2.20 on 2023-10-06 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_phone_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='with_facebook',
        ),
        migrations.RemoveField(
            model_name='user',
            name='with_google',
        ),
    ]
