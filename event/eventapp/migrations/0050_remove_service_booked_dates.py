# Generated by Django 4.2.4 on 2024-02-08 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0049_rename_dates_available_service_booked_dates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='booked_dates',
        ),
    ]
