from django.db import models
from accounts.validator import year_validator
from accounts.models import User
from django.utils.translation import ugettext_lazy as _

from core.models import Instagram


class Partners(models.Model):
    partner_year = models.PositiveSmallIntegerField(_('짝지 연도'), validators=[year_validator])
    partner_semester = models.PositiveSmallIntegerField(_('짝지 학기'), choices=User.SEMESTER_CHOICE)
    up_partner = models.ForeignKey('accounts.ActiveUser', on_delete=models.CASCADE, limit_choices_to={'is_new': False})
    down_partner_1 = models.ForeignKey('accounts.ActiveUser',
                                       on_delete=models.SET_NULL,
                                       limit_choices_to={'is_new': True},
                                       related_name='partners1',
                                       blank=True, null=True)
    down_partner_2 = models.ForeignKey('accounts.ActiveUser',
                                       on_delete=models.SET_NULL,
                                       limit_choices_to={'is_new': True},
                                       related_name='partners2',
                                       blank=True, null=True)
    down_partner_3 = models.ForeignKey('accounts.ActiveUser',
                                       on_delete=models.SET_NULL,
                                       limit_choices_to={'is_new': True},
                                       related_name='partners3',
                                       blank=True, null=True)
    score = models.SmallIntegerField(_('짝지 점수'), default=0)

    def raise_score(self, score):
        self.score += score
        self.save()


class PartnerMeeting(Instagram):
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    num_coffee = models.SmallIntegerField(_('마신 커피 수'), default=0)
    num_eat = models.SmallIntegerField(_('먹은 식사 수'), default=0)
