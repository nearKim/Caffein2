from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from core.mixins import TimeStampedMixin
from .fields import ThumbnailImageField


def get_album_photo_path(instance, filename):
    return 'media/photo_albums/{:%Y/%m/%d}/{}'.format(now(), filename)


class Album(TimeStampedMixin):
    name = models.CharField(_('앨범 이름'), max_length=50)
    description = models.CharField(_('설명'), max_length=100, blank=True)

    class Mete:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('photo_albums:album_detail', args=(self.id,))


class Photo(TimeStampedMixin):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    description = models.CharField(_('설명'), max_length=255, blank=True)
    # 파일이 입력되면서 썸네일이 만들어짐
    file = ThumbnailImageField(_('이미지'), upload_to=get_album_photo_path)

    class Meta:
        ordering = ['-created']
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo_albums:photo_detail', args=(self.id,))
