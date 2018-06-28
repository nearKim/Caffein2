from django.db import models
from core.models import (
    Instable,
    Postable,
)
from django.utils.translation import ugettext_lazy as _


class Meeting(Postable):
    meeting_date = models.DateTimeField(_('날짜 및 시간'))
    max_participants = models.PositiveIntegerField(_('참석 인원'), blank=True)
    participants = models.ManyToManyField('accounts.ActiveUser', verbose_name='참석자')

    def can_participate(self):
        return self.max_participants >= self.participants
