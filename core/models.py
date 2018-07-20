from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from .mixins import (
    TimeStampedMixin,
    Postable,
)


class Instagram(Postable):
    pass


def get_feed_photo_path(instance, filename):
    # FIXME: Uploader information must be set in the path
    return 'media/feed/{:%Y/%m/%d}/{}'.format(now(), filename)


class FeedPhotos(TimeStampedMixin):
    image = models.ImageField(upload_to=get_feed_photo_path)
    instagram = models.ForeignKey('core.Instagram', default=None, related_name='photos', verbose_name=_('인스타'),
                                  on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('피드 사진')
        verbose_name_plural = _('피드 사진')


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        obj_id = instance.id
        qs = super(CommentManager, self).filter(id=obj_id)
        return qs


class Comment(Postable):
    instagram = models.ForeignKey('core.Instagram', default=None, null=True, blank=True, related_name='comments',
                                  on_delete=models.CASCADE)
    meeting = models.ForeignKey('meetings.Meeting', default=None, null=True, blank=True, related_name='comments',
                                on_delete=models.CASCADE)
    objects = CommentManager()

    class Meta:
        verbose_name = _('댓글')
        verbose_name_plural = _('댓글')

    def __str__(self):
        return self.content

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.instagram is None and self.meeting is None:
            # Don't save
            return
        super(Comment, self).save()


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

    semester_start = models.DateField(_('학기 시작일'), help_text=_('1학기는 3월 2일, 2학기는 9월 1일'))
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

    @property
    def current_semester(self):
        return 1 if self.semester_start.month == 3 else 2

    @property
    def current_year(self):
        return self.semester_start.year

    @staticmethod
    def latest():
        return OperationScheme.objects.latest('id')

    @staticmethod
    def can_new_register():
        latest_os = OperationScheme.latest()
        if latest_os.new_register_end:
            return latest_os.new_register_end > now() > latest_os.new_register_start
        else:
            return now() > OperationScheme.latest().new_register_start

    @staticmethod
    def can_old_register():
        latest_os = OperationScheme.latest()
        if latest_os.old_register_end:
            return latest_os.old_register_end > now() > latest_os.old_register_start
        else:
            return now() > OperationScheme.latest().old_register_start
