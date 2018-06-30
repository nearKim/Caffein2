# Generated by Django 2.0.6 on 2018-06-30 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('posting_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Posting')),
                ('meeting_date', models.DateTimeField(verbose_name='날짜 및 시간')),
                ('max_participants', models.PositiveIntegerField(default=0, help_text='인원제한을 없애려면 0으로 설정하세요.', verbose_name='참석 인원')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.posting',),
        ),
        migrations.CreateModel(
            name='CoffeeEducation',
            fields=[
                ('meeting_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='meetings.Meeting')),
                ('category', models.CharField(choices=[('d', '드립 교육'), ('c', '커핑 교육'), ('e', '에스프레소 교육'), ('a', '운영진 교육')], max_length=1, verbose_name='분류')),
                ('difficulty', models.CharField(choices=[('e', '기초'), ('h', '심화')], max_length=1, verbose_name='난이도')),
                ('location', models.CharField(blank=True, max_length=50, verbose_name='장소')),
            ],
            options={
                'abstract': False,
            },
            bases=('meetings.meeting',),
        ),
        migrations.CreateModel(
            name='CoffeeMeeting',
            fields=[
                ('meeting_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='meetings.Meeting')),
            ],
            options={
                'abstract': False,
            },
            bases=('meetings.meeting',),
        ),
        migrations.CreateModel(
            name='OfficialMeeting',
            fields=[
                ('meeting_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='meetings.Meeting')),
                ('category', models.CharField(choices=[('i', '동소제'), ('w', '신환회'), ('m', 'MT'), ('k', '장터')], max_length=1, verbose_name='분류')),
                ('location', models.CharField(blank=True, max_length=50, verbose_name='행사 장소')),
            ],
            options={
                'abstract': False,
            },
            bases=('meetings.meeting',),
        ),
        migrations.AddField(
            model_name='meeting',
            name='participants',
            field=models.ManyToManyField(to='accounts.ActiveUser', verbose_name='참석자'),
        ),
    ]