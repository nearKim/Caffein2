# Generated by Django 2.0.6 on 2018-07-09 11:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_auto_20180709_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activeuser',
            options={'get_latest_by': ['-active_year', 'active_semester'], 'verbose_name': '활동 회원',
                     'verbose_name_plural': '활동 회원'},
        ),
    ]