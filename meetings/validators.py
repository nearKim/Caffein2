import re

from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


def meeting_date_validator(value):
    if value < timezone.now():
        # if value < timezone.localtime():
        raise ValidationError(_('모임 일시는 지금보다 이전일 수 없습니다.'))
