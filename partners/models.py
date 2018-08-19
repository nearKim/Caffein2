from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from accounts.validator import year_validator
from core.models import Instagram, OperationScheme


class Partners(models.Model):
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

    def raise_score(self, score):
        self.score += score
        self.save()

    @staticmethod
    def related_partner(user):
        # input 파라미터 user가 속한 짝지 중 가장 최신의 객체를 반환합니다.
        try:
            related = Partners.objects.filter(
                Q(up_partner__user=user) |
                Q(down_partner_1__user=user) |
                Q(down_partner_2__user=user) |
                Q(down_partner_3__user=user)
            ).latest()
        except Partners.DoesNotExist:
            related = None
        return related


class PartnerMeeting(Instagram):
    partner = models.ForeignKey('partners.Partners', on_delete=models.CASCADE)
    num_coffee = models.SmallIntegerField(_('마신 커피 수'), default=0)
    num_eat = models.SmallIntegerField(_('먹은 식사 수'), default=0)

    class Meta:
        verbose_name = _('짝지 모임')
        verbose_name_plural = _('짝지 모임')

    def get_absoulute_url(self):
        return reverse('partners:meeting-list')

    def save(self):
        if not self.pk:
            # https://stackoverflow.com/questions/2307943/django-overriding-the-model-create-method
            latest_os = OperationScheme.latest()
            coffee_score, eat_score = latest_os.coffee_point, latest_os.eat_point
            self.partner.raise_score(coffee_score * self.num_coffee + eat_score * self.num_eat)
        super().save()
