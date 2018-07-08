from django.db import models
from core.models import Instagram
from django.utils.translation import ugettext_lazy as _


class Meeting(Instagram):
    title = models.CharField(_('제목'), max_length=20, blank=True)
    meeting_date = models.DateTimeField(_('날짜 및 시간'))
    max_participants = models.SmallIntegerField(_('참석 인원'), default=0, help_text=_('인원제한을 없애려면 0으로 설정하세요.'))
    participants = models.ManyToManyField('accounts.ActiveUser', verbose_name='참석자')

    class Meta:
        verbose_name = _('모임')
        verbose_name_plural = _('모임')

    def can_participate(self):
        if self.max_participants == 0:
            return True
        else:
            return self.max_participants > self.participants.count()

    def count_participants(self):
        return self.participants.count()


class OfficialMeeting(Meeting):
    INTRODUCTION, WELCOME, MT, MARKET = 'i', 'w', 'm', 'k'
    EVENT_CATEGORY = (
        (INTRODUCTION, '동소제'),
        (WELCOME, '신환회'),
        (MT, 'MT'),
        (MARKET, '장터')
    )

    category = models.CharField(_('분류'), max_length=1, choices=EVENT_CATEGORY)
    # TODO: Add navermap / googlemap functionality
    location = models.CharField(_('행사 장소'), max_length=50, blank=True)

    class Meta:
        verbose_name = _('공식 모임')
        verbose_name_plural = _('공식 모임')


class CoffeeEducation(Meeting):
    DRIP, CUPPING, ESPRESSO, ADMIN = 'd', 'c', 'e', 'a'
    EASY, HARD = 'e', 'h'

    EDUCATION_CHOICES = (
        (DRIP, '드립 교육'),
        (CUPPING, '커핑 교육'),
        (ESPRESSO, '에스프레소 교육'),
        (ADMIN, '운영진 교육')
    )
    DIFFICULTY_CHOICES = (
        (EASY, '기초'),
        (HARD, '심화')
    )

    category = models.CharField(_('분류'), max_length=1, choices=EDUCATION_CHOICES)
    difficulty = models.CharField(_('난이도'), max_length=1, choices=DIFFICULTY_CHOICES)
    # TODO: Add navermap / googlemap functionality
    location = models.CharField(_('장소'), max_length=50, blank=True)

    class Meta:
        verbose_name = _('커피 교육')
        verbose_name_plural = _('커피 교육')


class CoffeeMeeting(Meeting):
    pass
    # TODO: Add cafe app
