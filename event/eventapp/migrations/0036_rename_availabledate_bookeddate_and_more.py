# Generated by Django 4.2.4 on 2024-01-30 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0035_alter_availabledate_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AvailableDate',
            new_name='BookedDate',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='available_dates',
            new_name='booked_dates',
        ),
    ]
