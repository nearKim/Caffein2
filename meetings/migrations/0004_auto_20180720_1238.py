# Generated by Django 2.0.6 on 2018-07-20 03:38

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('meetings', '0003_auto_20180720_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 20, 3, 38, 35, 71968, tzinfo=utc),
                                       verbose_name='날짜 및 시간'),
        ),
    ]