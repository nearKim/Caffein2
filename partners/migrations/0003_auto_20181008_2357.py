# Generated by Django 2.0.6 on 2018-10-08 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0002_coffeemeetingfeed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coffeemeetingfeed',
            options={'verbose_name': '커모 후기', 'verbose_name_plural': '커모 후기'},
        ),
        migrations.AlterField(
            model_name='coffeemeetingfeed',
            name='coffee_meeting',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='meetings.CoffeeMeeting', verbose_name='커모'),
        ),
    ]