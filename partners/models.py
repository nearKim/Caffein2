from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from accounts.models import User, ActiveUser
from accounts.validators import year_validator
from core.models import Instagram, OperationScheme


class Partner(models.Model):
    partner_year = models.PositiveSmallIntegerField(_('짝지 연도'), validators=[year_validator])
    partner_semester = models.PositiveSmallIntegerField(_('짝지 학기'), choices=User.SEMESTER_CHOICE)
    up_partner = models.ForeignKey('accounts.ActiveUser', on_delete=models.CASCADE)
    down_partner_1 = models.ForeignKey('accounts.ActiveUser',
                                       on_delete=models.SET_NULL,
                                       related_name='partners1',
                                       blank=True, null=True)
    down_partner_2 = models.ForeignKey('accounts.ActiveUser',
                                       on_delete=models.SET_NULL,
                                       related_name='partners2',
                                       blank=True, null=True)
    down_partner_3 = models.ForeignKey('accounts.ActiveUser',
                                       on_delete=models.SET_NULL,
                                       related_name='partners3',
                                       blank=True, null=True)
    score = models.FloatField(_('짝지 점수'), default=0.0)

    class Meta:
        verbose_name = _('짝지')
        verbose_name_plural = _('짝지')
        unique_together = ['partner_year', 'partner_semester', 'up_partner']
        get_latest_by = ['-partner_year', 'partner_semester']

    def __str__(self):
        return "{}년 {}학기 기존({})".format(self.partner_year, self.partner_semester, self.up_partner.user.name)

    def containing_active_users(self):
        # 짝지 객체에 속한 모든 구성원들의 set을 반환한다.
        return {self.up_partner, self.down_partner_1, self.down_partner_2, self.down_partner_3}

    def down_partner_count(self):
        return len(self.containing_active_users() - set([None])) - 1

    def raise_score(self, score):
        latest_os = OperationScheme.latest()
        if latest_os.semester_end:
            if now() > latest_os.semester_end:
                # 학기가 종료된 후에는 짝지점수를 올리면 안된다.
                return
        self.score += score
        self.save()

    @staticmethod
    def current_activeuser_set():
        # 최신의 운영정보를 불러온다
        latest_os = OperationScheme.latest()
        # 현재 학기, 연도에 대항하는 모든 짝지 객체를 불러온다
        current_partners = Partner.objects \
            .select_related('up_partner') \
            .select_related('down_partner_1') \
            .select_related('down_partner_2') \
            .select_related('down_partner_3') \
            .filter(partner_semester=latest_os.current_semester, partner_year=latest_os.current_year)

        # 만일 하나도 없다면 None을 반환한다
        if not current_partners.exists():
            return ActiveUser.objects.none()
        # 존재한다면 각 짝지객체에 속한 모든 ActiveUser객체들을 얻는다
        activeusers = set()
        for partner in current_partners:
            activeusers = activeusers | partner.containing_active_users()
        activeuser_pks = [activeuser.pk for activeuser in activeusers if activeuser is not None]

        return ActiveUser.objects.select_related('user').filter(id__in=activeuser_pks)

    @staticmethod
    def related_partner_user(user):
        # input 파라미터 user가 속한 짝지 중 가장 최신의 객체를 반환한다.
        try:
            related = Partner.objects \
                .select_related('up_partner') \
                .select_related('down_partner_1') \
                .select_related('down_partner_2') \
                .select_related('down_partner_3') \
                .select_related('up_partner__user') \
                .select_related('down_partner_1__user') \
                .select_related('down_partner_2__user') \
                .select_related('down_partner_3__user') \
                .filter(
                Q(up_partner__user=user) |
                Q(down_partner_1__user=user) |
                Q(down_partner_2__user=user) |
                Q(down_partner_3__user=user)
            ).latest()
        except Partner.DoesNotExist:
            related = None
        return related

    @staticmethod
    def related_partner_activeuser(active_user):
        # input 파라미터 active_user가 속한 짝지 중 가장 최신의 객체를 반환한다.
        try:
            related = Partner.objects \
                .select_related('up_partner') \
                .select_related('down_partner_1') \
                .select_related('down_partner_2') \
                .select_related('down_partner_3') \
                .select_related('up_partner__user') \
                .select_related('down_partner_1__user') \
                .select_related('down_partner_2__user') \
                .select_related('down_partner_3__user') \
                .filter(
                Q(up_partner=active_user) |
                Q(down_partner_1=active_user) |
                Q(down_partner_2=active_user) |
                Q(down_partner_3=active_user)
            ).latest()
        except Partner.DoesNotExist:
            related = None
        return related


class PartnerMeeting(Instagram):
    partner = models.ForeignKey('partners.Partner', on_delete=models.CASCADE)
    num_coffee = models.SmallIntegerField(_('마신 커피 수'), default=0)
    num_eat = models.SmallIntegerField(_('먹은 식사 수'), default=0)

    class Meta:
        verbose_name = _('짝지 모임')
        verbose_name_plural = _('짝지 모임')

    def __str__(self):
        return "{}의 짝모({})".format(self.partner, self.created.strftime("%m월 %d일"))

    def get_absoulute_url(self):
        return reverse('partners:meeting-list')

    def save(self):
        if not self.pk:
            # https://stackoverflow.com/questions/2307943/django-overriding-the-model-create-method
            latest_os = OperationScheme.latest()
            coffee_score, eat_score = latest_os.coffee_point, latest_os.eat_point
            self.partner.raise_score(coffee_score * self.num_coffee + eat_score * self.num_eat)
        super().save()


class CoffeeMeetingFeed(Instagram):
    coffee_meeting = models.OneToOneField('meetings.CoffeeMeeting', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '커모 후기'
        verbose_name_plural = '커모 후기'

    def __str__(self):
        return self.coffee_meeting.__str__()
