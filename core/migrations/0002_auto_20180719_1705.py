# Generated by Django 2.0.6 on 2018-07-19 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='instagram',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='comments', to='core.Instagram'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='meeting',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='comments', to='meetings.Meeting'),
        ),
    ]
