from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from core.mixins import TimeStampedMixin
from django.conf import settings

from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail


def get_album_photo_path(instance, filename):
    return 'media/photo_albums/{:%Y/%m/%d}/{}'.format(now(), filename)


class Album(TimeStampedMixin):
    name = models.CharField(_('앨범 이름'),
                            max_length=50)
    description = models.CharField(_('설명'),
                                   max_length=100,
                                   blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='album_uploader')

    class Mete:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('photo_albums:album_detail', args=(self.id,))


class Photo(TimeStampedMixin):
    album = models.ForeignKey(Album,
                              on_delete=models.CASCADE,
                              null=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='photo_uploader')

    file = models.ImageField(_('이미지'), upload_to=get_album_photo_path)

    thumbnail = ImageSpecField(
        source='file',
        processors=[Thumbnail(128, 128)],
        format='JPEG',
        options={'quality': 60}
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return reverse('photo_albums:photo_detail', args=(self.id,))


