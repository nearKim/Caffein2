from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from core.mixins import TimeStampedMixin, Postable
from core.models import Comment


class Meeting(Postable):
    title = models.CharField(_('제목'), max_length=20, blank=True)
    # FIXME: Delete Default timezone and add datetime picker widget
    meeting_date = models.DateTimeField(_('날짜 및 시간'), default=timezone.now())
    max_participants = models.PositiveSmallIntegerField(_('참석 인원'), default=0, help_text=_('인원제한을 없애려면 0으로 설정하세요.'))
    participants = models.ManyToManyField('accounts.ActiveUser', verbose_name='참석자')

    class Meta:
        verbose_name = _('모임')
        verbose_name_plural = _('모임')
        get_latest_by = ['-meeting_date']

    # For polymorphism
    # https://stackoverflow.com/a/13306529
    def get_class_name(self):
        return str(self.__class__.__name__).lower()

    def cast(self):
        for name in dir(self):
            try:
                attr = getattr(self, name)
                if isinstance(attr, self.__class__):
                    return attr
            except:
                pass
        return self

    # General Use methods
    def can_participate(self):
        if self.max_participants == 0:
            return True
        else:
            return self.max_participants > self.participants.count()

    def count_participants(self):
        return self.participants.count()

    def participate_meeting(self, active_user):
        if self.can_participate():
            self.participants.add(active_user)
            return True
        else:
            return False

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    def save(self, *args, **kwargs):
        if not self.can_participate():
            return
        else:
            super().save(*args, **kwargs)


def get_meeting_photo_path(instance, filename):
    return 'media/meeting/{:%Y/%m/%d}/{}'.format(now(), filename)


class MeetingPhotos(TimeStampedMixin):
    image = models.ImageField(upload_to=get_meeting_photo_path)
    meeting = models.ForeignKey('meetings.Meeting', related_name='photos', verbose_name=_('모임'),
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('모임 사진')
        verbose_name_plural = _('모임 사진')


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
    # TODO: Add navermap / googlemap functionality
    location = models.CharField(_('장소'), max_length=50, blank=True)

    class Meta:
        verbose_name = _('커피 교육')
        verbose_name_plural = _('커피 교육')

    def get_absolute_url(self):
        return reverse('meetings:education-detail', args=[self.pk])


class CoffeeMeeting(Meeting):
    pass
    # TODO: Add cafe app
