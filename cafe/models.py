from django.db import models
from django.utils.timezone import now
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
# Create your models here.

class Cafe(models.Model):
    PRICE_CATEGORY = (
        ('CHEAPEST', '~ 5천원'),
        ('CHEAP', '5천원 ~ 만원'),
        ('MIDDLE', '만원 ~ 2만원'),
        ('EXPENSIVE', '2만원 ~ '),
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
    address = models.CharField(_('주소'), max_length=100, null=True)
    phone = models.CharField(_('전화번호'), max_length=14, null=True,
                             help_text=_('0x-xxxx-xxxx 형식으로 입력해주세요'))
    machine = models.CharField(_('에스프레소 머신'), max_length=100, null=True)
    grinder = models.CharField(_('그라인더'), max_length=100, null=True)
    price = models.CharField(_('가격대'), max_length=10, choices=PRICE_CATEGORY)

    from_time = models.DateTimeField(_('개장시간'), null=True)
    to_time = models.DateTimeField(_('폐장시간'), null=True)

    closed_day = models.CharField(_('휴무일'), choices=DAY_CATEGORY, max_length=3, null=True)
    closed_frq = models.CharField(_('휴무 빈도'), choices=FRQ_CATEGORY, max_length=6, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')

    def __str__(self):
        return self.name

