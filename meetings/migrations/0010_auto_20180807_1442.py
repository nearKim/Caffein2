# Generated by Django 2.0.6 on 2018-08-07 05:42

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_auto_20180807_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 7, 5, 42, 3, 79035, tzinfo=utc), verbose_name='날짜 및 시간'),
        ),
    ]
