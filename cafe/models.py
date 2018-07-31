from django.db import models
from django.utils.timezone import now
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from core.mixins import TimeStampedMixin
# Create your models here.

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
    FRQ_CATEGORY = (
        ('EVERY', '매주'),
        ('FIRST', '첫번째'),
        ('SECOND', '두번째'),
        ('THIRD', '세번째'),
        ('FOURTH', '네번째'),
        ('LAST', '마지막')
    )

    name = models.CharField(_('카페이름'), max_length=50, unique=True)
    address = models.CharField(_('주소'), max_length=100)
    phone = models.CharField(_('전화번호'), max_length=14, null=True,
                             help_text=_('0x-xxxx-xxxx 형식으로 입력해주세요'))
    machine = models.CharField(_('에스프레소 머신'), max_length=100, null=True)
    grinder = models.CharField(_('그라인더'), max_length=100, null=True)
    price = models.CharField(_('가격대'), max_length=15, choices=PRICE_CATEGORY)

    from_time = models.TimeField(_('개점시간'), null=True)
    to_time = models.TimeField(_('폐점시간'), null=True)

    closed_day = models.CharField(_('휴무일'), choices=DAY_CATEGORY, max_length=3, null=True)
    closed_frq = models.CharField(_('휴무 빈도'), choices=FRQ_CATEGORY, max_length=6, null=True)
    closed_holiday = models.BooleanField(_('공휴일 휴무 여부'), default=False)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')

    def __str__(self):
        return self.name

