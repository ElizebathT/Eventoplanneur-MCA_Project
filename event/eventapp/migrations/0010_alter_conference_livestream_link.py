# Generated by Django 4.2.4 on 2023-09-18 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0009_webinarregistration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='livestream_link',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
