from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from core.models import Meeting, OperationScheme
from accounts.models import ActiveUser


class OfficialMeeting(Meeting):
    INTRODUCTION, WELCOME, MT, MARKET, ETC = 'i', 'w', 'm', 'k', 'e'
    EVENT_CATEGORY = (
        (INTRODUCTION, '동소제'),
        (WELCOME, '신환회'),
        (MT, 'MT'),
        (MARKET, '장터'),
        (ETC, '기타')
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
    cafe = models.ForeignKey('cafes.Cafe', on_delete=models.SET_NULL, verbose_name=_('카페'), null=True)

    class Meta:
        verbose_name = _('커모')
        verbose_name_plural = _('커모')

    def get_absolute_url(self):
        return reverse('meetings:coffee-meeting-detail', args=[self.pk])

    def __str__(self):
        return "{} {} 커모".format(self.meeting_date.strftime("%Y년 %m월 %d일 %H시 %M분"), self.cafe.name)

    def update_partner_score(self):
        from partners.models import Partner
        latest_os = OperationScheme.latest()
        # 현재 참여하고자 하는 active user의 가장 최신의 짝지 객체를 가져온다
        for active_user in self.participants.all():
            related_partner = Partner.related_partner_activeuser(active_user)
            if related_partner is None:
                # related partner가 없으면(운영자계정, 신입회원 등) 아무것도 하지 않는다
                continue

            # 짝지 년도, 학기를 가장 최신의 운영정보 년도, 학기와 비교한다
            if not (related_partner.partner_year == latest_os.current_year
                    and related_partner.partner_semester == latest_os.current_semester):
                # 만일 다르다면 아무것도 하지 않는다. 신학기에 예전학기 짝지 정보를 불러온 것이기 때문이다.
                continue

            else:
                from meetings.models import CoffeeMeeting
                # 참여였을 경우 원하는 점수만큼(현재는 커피 한잔 점수) 올린다. 단 커모 개최자는 추가점수를 준다.
                if active_user == ActiveUser.objects.filter(user=self.author).latest():
                    related_partner.raise_score(latest_os.coffee_point + latest_os.extra_author_point)
                else:
                    related_partner.raise_score(latest_os.coffee_point)
