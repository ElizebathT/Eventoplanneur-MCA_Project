# Generated by Django 4.2.4 on 2024-01-19 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0030_alter_service_locations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='locations',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.AddField(
            model_name='service',
            name='locations',
            field=models.TextField(null=True),
        ),
    ]
