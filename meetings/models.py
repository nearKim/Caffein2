from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from core.mixins import TimeStampedMixin, Postable
from comments.models import Comment
from core.models import Meeting


class OfficialMeeting(Meeting):
    INTRODUCTION, WELCOME, MT, MARKET = 'i', 'w', 'm', 'k'
    EVENT_CATEGORY = (
        (INTRODUCTION, '동소제'),
        (WELCOME, '신환회'),
        (MT, 'MT'),
        (MARKET, '장터')
    )

    category = models.CharField(_('분류'), max_length=1, choices=EVENT_CATEGORY)
    # 네이버맵
    location = models.CharField(_('행사 장소'), max_length=50, blank=True)
    mapx = models.IntegerField(_('x좌표'), null=True, blank=True)
    mapy = models.IntegerField(_('y좌표'), null=True, blank=True)

    class Meta:
        verbose_name = _('공식 모임')
        verbose_name_plural = _('공식 모임')

    def __str__(self):
        return "{}({})".format(self.get_category_display(), self.meeting_date.strftime("%Y년 %m월 %d일 %H시 %M분"))

    def get_absolute_url(self):
        return reverse('meetings:official-detail', args=[self.pk])


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

    # 네이버맵
    location = models.CharField(_('교육 장소'), max_length=50, blank=True)
    mapx = models.IntegerField(_('x좌표'), null=True, blank=True)
    mapy = models.IntegerField(_('y좌표'), null=True, blank=True)

    class Meta:
        verbose_name = _('커피 교육')
        verbose_name_plural = _('커피 교육')

    def __str__(self):
        return "{} {}({})".format(self.get_category_display(), self.get_difficulty_display(),
                                  self.meeting_date.strftime("%Y년 %m월 %d일 %H시 %M분"))

    def get_absolute_url(self):
        return reverse('meetings:education-detail', args=[self.pk])


class CoffeeMeeting(Meeting):
    cafe = models.ForeignKey('cafe.Cafe', on_delete=models.SET_NULL, verbose_name=_('카페'), null=True)

    class Meta:
        verbose_name = _('커모')
        verbose_name_plural = _('커모')

    def get_absolute_url(self):
        return reverse('meetings:coffee-meeting-detail', args=[self.pk])

    def __str__(self):
        return "{}({})".format(self.cafe.name, self.meeting_date.strftime("%Y년 %m월 %d일 %H시 %M분"))
