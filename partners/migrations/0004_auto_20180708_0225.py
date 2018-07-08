# Generated by Django 2.0.6 on 2018-07-08 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0003_auto_20180701_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partners',
            name='down_partner_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partners1', to='accounts.ActiveUser'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='down_partner_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partners2', to='accounts.ActiveUser'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='down_partner_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partners3', to='accounts.ActiveUser'),
        ),
    ]
