from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from core.mixins import TimeStampedMixin


def get_cafe_photo_path(instance, filename):
    return 'cafes/{:%Y/%m/%d}/{}'.format(now(), filename)


class Cafe(TimeStampedMixin):
    PRICE_CATEGORY = (
        ('CHEAPEST', '~ 2천원'),
        ('CHEAP', '2천원 ~ 4천원'),
        ('MIDDLE', '4천원 ~ 6천원'),
        ('EXPENSIVE', '6천원 ~ 8천원'),
        ('MOST EXPENSIVE', '8천원 ~ '),
    )
    DAY_CATEGORY = (
        ('SUN', '일요일'),
        ('MON', '월요일'),
        ('TUE', '화요일'),
        ('WED', '수요일'),
        ('THU', '목요일'),
        ('FRI', '금요일'),
        ('SAT', '토요일'),
    )

    name = models.CharField(_('카페이름'), max_length=50)
    address = models.CharField(_('주소'), max_length=200)
    description = models.TextField(_('설명'), blank=True)
    phone = models.CharField(_('전화번호'), max_length=14, blank=True)
    machine = models.CharField(_('에스프레소 머신'), max_length=100, blank=True)
    grinder = models.CharField(_('그라인더'), max_length=100, blank=True)
    price = models.CharField(_('가격대'), max_length=15, choices=PRICE_CATEGORY, blank=True)

    from_time = models.TimeField(_('개점시간'), null=True, blank=True)
    to_time = models.TimeField(_('폐점시간'), null=True, blank=True)

    closed_day = models.CharField(_('휴무일'), choices=DAY_CATEGORY, max_length=3, blank=True)
    closed_holiday = models.BooleanField(_('공휴일 휴무 여부'))
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='uploader')
    # image = models.ImageField(_('이미지'), upload_to=get_cafe_photo_path, blank=True)

    # naver api
    link = models.CharField(_('홈페이지'), validators=[URLValidator()], blank=True, max_length=260)
    road_address = models.CharField(_('도로명주소'), max_length=100, blank=True)
    mapx = models.IntegerField(_('x좌표'), null=True, blank=True)
    mapy = models.IntegerField(_('y좌표'), null=True, blank=True)

    class Meta:
        ordering = ['-created']
        unique_together = ['name', 'address']
        verbose_name = _('카페')
        verbose_name_plural = _('카페')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cafes:cafes-detail', args=[str(self.id)])


class CafePhoto(models.Model):
    image = ProcessedImageField(upload_to=get_cafe_photo_path,
                                processors=[ResizeToFill(300, 340)],
                                format='JPEG',
                                options={'quality': 60},
                                verbose_name=_('카페 사진'))
    cafe = models.ForeignKey('cafes.Cafe', related_name='photos', on_delete=models.CASCADE, verbose_name=_('카페'))

    class Meta:
        verbose_name = _('카페 사진')
        verbose_name_plural = _('카페 사진')
