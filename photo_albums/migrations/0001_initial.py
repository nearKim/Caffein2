# Generated by Django 2.0.6 on 2018-09-02 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import photo_albums.fields
import photo_albums.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='앨범 이름')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='설명')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='album_uploader', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('file', photo_albums.fields.ThumbnailImageField(upload_to=photo_albums.models.get_album_photo_path)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='photo_albums.Album')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photo_uploader', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
                'ordering': ['-created'],
            },
        ),
    ]