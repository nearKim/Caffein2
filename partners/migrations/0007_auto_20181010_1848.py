# Generated by Django 2.0.6 on 2018-10-10 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0006_partnermeeting_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnermeeting',
            name='point',
            field=models.FloatField(default=0.0),
        ),
    ]
