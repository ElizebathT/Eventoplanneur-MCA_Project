# Generated by Django 4.2.4 on 2024-02-02 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0038_service_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='org_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
