from django.db import models

from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from .mixins import (
    TimeStampedMixin,
    Instable,
    Postable
)


class Instagram(Instable):
    pass


class Posting(Postable):
    pass


def get_feed_photo_path(instance, filename):
    user_id = instance.pk
    return 'feed_images/{}/{:%Y/%m/%d}/{}'.format(user_id, now(), filename)


def get_posted_photo_path(instance, filename):
    user_id = instance.pk
    return 'post_images/{}/{:%Y/%m/%d}/{}'.format(user_id, now(), filename)


class FeedPhotos(models.Model):
    image = models.ImageField(upload_to=get_feed_photo_path)
    instagram = models.ForeignKey(Instagram, default=None, on_delete=models.CASCADE)


class PostedPhotos(models.Model):
    image = models.ImageField(upload_to=get_posted_photo_path)
    posting = models.ForeignKey(Posting, default=None, on_delete=models.CASCADE)


class OperationScheme(models.Model):
    BANK_CHOICES = (
        ('kb', 'KB국민은행'),
        ('nh', 'NH농협'),
        ('sh', '신한은행'),
        ('wr', '우리은행'),
        ('hn', '하나(구 외환)'),
        ('kk', '케이뱅크'),
        ('ka', '카카오뱅크'),
        ('kd', 'KDB산업은행'),
        ('ib', 'IBK기업은행'),
        ('sh', '수협은행'),
        ('sm', '새마을금고')
    )

    semester_start = models.DateField(_('학기 시작일'))
    # 학기 종료일 = 짝지 마감일
    semester_end = models.DateField(_('학기 종료일'), blank=True, null=True, default=None)

    new_register_start = models.DateTimeField(_('신입 가입 시작일'))
    new_register_end = models.DateTimeField(_('신입 가입 종료일'))
    old_register_start = models.DateTimeField(_('기존 가입 시작일'))
    old_register_end = models.DateTimeField(_('기존 가입 종료일'))

    coffee_point = models.FloatField(_('커모 1회당 점수'), default=2.0, help_text=_('실수형 점수입니다. 예: 2.0'))
    eat_point = models.FloatField(_('밥모 1회당 점수'), default=1.0, help_text=_('실수형 점수입니다. 예: 2.0'))

    bank_account = models.CharField(_('입금 계좌'), max_length=30)
    bank = models.CharField(_('입금 은행'), choices=BANK_CHOICES, max_length=2)

    # 어떠한 일이 있어도 이 relation의 tuple 정보는 삭제되면 안됨
    # 피치 못할 경우 동일인이 회장을 2회 할 가능성 존재
    boss = models.ForeignKey('accounts.ActiveUser', on_delete=models.DO_NOTHING)

    new_pay = models.PositiveIntegerField(_('신입회원 가입비'))
    old_pay = models.PositiveIntegerField(_('기존회원 가입비'))

    class Meta:
        verbose_name = _('운영 정보')
        verbose_name_plural = _('운영 정보')

    @staticmethod
    def latest():
        return OperationScheme.objects.latest('id')
