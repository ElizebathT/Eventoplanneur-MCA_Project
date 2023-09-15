# Generated by Django 4.2.4 on 2023-09-13 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0004_conference_org_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='conference',
            name='speakers',
            field=models.ManyToManyField(blank=True, to='eventapp.speaker'),
        ),
    ]
