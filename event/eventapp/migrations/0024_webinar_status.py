# Generated by Django 4.2.4 on 2023-09-30 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0023_attendee_org_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]