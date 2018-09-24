from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from comments.models import Comment

from .mixins import (
    TimeStampedMixin,
    Postable,
)


def get_feed_photo_path(instance, filename):
    # FIXME: Uploader information must be set in the path
    return 'media/feed/{:%Y/%m/%d}/{}'.format(now(), filename)


def get_meeting_photo_path(instance, filename):
    return 'media/meeting/{:%Y/%m/%d}/{}'.format(now(), filename)


class Instagram(Postable):
    pass


class Meeting(Postable):
    title = models.CharField(_('제목'), max_length=50, blank=True)
    meeting_date = models.DateTimeField(_('날짜 및 시간'))
    max_participants = models.PositiveSmallIntegerField(_('최대 참석인원'), default=0, help_text=_('인원제한을 없애려면 0으로 설정하세요.'))
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

    def update_partner_score(self, active_user, increment):
        # TODO: 커모, 교육 참가시 가산점 제도 확
        from partners.models import Partner
        # 현재 참여하고자 하는 active user의 가장 최신의 짝지 객체를 가져온다
        related_partner = Partner.related_partner_activeuser(active_user)
        if related_partner is None:
            # related partner가 없으면(운영자계정, 신입회원 등) 아무것도 하지 않는다
            return
        latest_os = OperationScheme.latest()
        # 짝지 년도, 학기를 가장 최신의 운영정보 년도, 학기와 비교한다
        if not (related_partner.partner_year == latest_os.current_year
                and related_partner.partner_semester == latest_os.current_semester):
            # 만일 다르다면 아무것도 하지 않는다. 신학기에 예전학기 짝지 정보를 불러온 것이기 때문이다.
            return

        else:
            # 같다면 짝지의 구성원이 현재 참여자에 존재하는지 확인한다.
            participants_set = {participant for participant in self.participants.all()}
            partner_in_meeting = related_partner.containing_active_users().intersection(participants_set)
            if len(partner_in_meeting) != 0:
                if increment:
                    # 참여였을 경우 원하는 점수만큼(현재는 커피 한잔 점수) 올린다.
                    related_partner.raise_score(latest_os.coffee_point)
                else:
                    # 참여취소일 경우 점수를 하향해야 한다.
                    related_partner.raise_score(-latest_os.coffee_point)

    def participate_or_not(self, active_user):
        if active_user in self.participants.all():
            # 참여 취소
            self.update_partner_score(active_user, False)
            self.participants.remove(active_user)
            return False
        else:
            self.update_partner_score(active_user, True)
            self.participants.add(active_user)
            return True

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs


class MeetingPhoto(TimeStampedMixin):
    image = models.ImageField(upload_to=get_meeting_photo_path, verbose_name=_('사진'))
    meeting = models.ForeignKey('core.Meeting', related_name='photos', verbose_name=_('모임'),
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('모임 사진')
        verbose_name_plural = _('모임 사진')

    def get_absolute_url(self):
        # 각 meeting의 디테일뷰로 이동
        return self.meeting.cast().get_absolute_url()

    def save(self, *args, **kwargs):
        # https://stackoverflow.com/a/49296707
        base = 1200
        img = Image.open(self.image)
        img_format = img.format
        (width, height) = img.size

        if width < base and height < base:
            factor = 1
        else:
            factor = base / width if base / width < base / height else base / height
        img = img.resize((int(width * factor), int(height * factor)), Image.ANTIALIAS)
        img_io = BytesIO()
        img.save(img_io, img_format, quality=60)
        self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)
        super(MeetingPhoto, self).save(*args, **kwargs)


class FeedPhoto(TimeStampedMixin):
    image = models.ImageField(upload_to=get_feed_photo_path, verbose_name=_('사진'))
    instagram = models.ForeignKey('core.Instagram', default=None, related_name='photos', verbose_name=_('인스타'),
                                  on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('피드 사진')
        verbose_name_plural = _('피드 사진')

    def get_absolute_url(self):
        # 인스타그램의 경우 짝모에서만 사용되므로 단일객체를 볼 필요 없이 바로 짝모리스트로 이동한다.
        return reverse('partners:meeting-list')

    def save(self, *args, **kwargs):
        # https://stackoverflow.com/a/49296707
        base = 1200
        img = Image.open(self.image)
        img_format = img.format
        (width, height) = img.size

        if width < base and height < base:
            factor = 1
        else:
            # 너비와 높이 중 큰쪽 대한 비율로 맞춘다.
            factor = base / width if base / width < base / height else base / height
        img = img.resize((int(width * factor), int(height * factor)), Image.ANTIALIAS)
        img_io = BytesIO()
        img.save(img_io, img_format, quality=60)
        self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)
        super(FeedPhoto, self).save(*args, **kwargs)


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
    new_register_end = models.DateTimeField(_('신입 가입 종료일'), blank=True, null=True)
    old_register_start = models.DateTimeField(_('기존 가입 시작일'))
    old_register_end = models.DateTimeField(_('기존 가입 종료일'), blank=True, null=True)

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

    def __str__(self):
        return "{}년 {}학기 운영정보".format(self.current_year, self.current_semester)

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
            return now() > latest_os.new_register_start

    @staticmethod
    def can_old_register():
        latest_os = OperationScheme.latest()
        if latest_os.old_register_end:
            return latest_os.old_register_end > now() > latest_os.old_register_start
        else:
            return now() > latest_os.old_register_start
