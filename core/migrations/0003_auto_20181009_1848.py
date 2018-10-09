# Generated by Django 2.0.6 on 2018-10-09 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20181007_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationscheme',
            name='limit_coffee',
            field=models.SmallIntegerField(default=3, help_text='정수형 점수입니다. 하루에 커모할 수 있는 횟수를 지정합니다.', verbose_name='1일 커모 제한 횟수'),
        ),
        migrations.AddField(
            model_name='operationscheme',
            name='limit_eat',
            field=models.SmallIntegerField(default=2, help_text='정수형 점수입니다. 하루에 밥모할 수 있는 횟수를 지정합니다.', verbose_name='1일 밥모 제한 횟수'),
        ),
    ]
