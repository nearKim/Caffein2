# Generated by Django 2.0.6 on 2018-07-19 08:05

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 19, 8, 5, 58, 533046, tzinfo=utc),
                                       verbose_name='날짜 및 시간'),
        ),
    ]