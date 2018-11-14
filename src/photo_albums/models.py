from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from pilkit.processors import ResizeToFill

from core.mixins import TimeStampedMixin, Postable
from core.models import rotate_and_resize
from django.conf import settings

from imagekit.models import ImageSpecField


def get_album_photo_path(instance, filename):
    return 'media/photo_albums/{:%Y/%m/%d}/{}'.format(now(), filename)


class Album(TimeStampedMixin):
    name = models.CharField(_('앨범 이름'),
                            max_length=50)
    description = models.CharField(_('설명'),
                                   max_length=100,
                                   blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='albums')

    class Meta:
        verbose_name = '사진첩'
        verbose_name_plural = '사진첩'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('photo_albums:album-detail', args=(self.id,))


class Photo(TimeStampedMixin):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, related_name='photos')
    description = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(_('사진'), upload_to=get_album_photo_path)
    thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 60}
    )

    class Meta:
        ordering = ['-created']
        verbose_name = '사진'
        verbose_name_plural = '사진'

    def save(self, *args, **kwargs):
        # https://stackoverflow.com/a/49296707
        img_io = rotate_and_resize(self.photo)
        self.photo.save(self.photo.name, ContentFile(img_io.getvalue()), save=False)
        super(Photo, self).save(*args, **kwargs)


# TODO: implement below
class PhotoComment(Postable):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = '사진 댓글'
        verbose_name_plural = '사진 댓글'
