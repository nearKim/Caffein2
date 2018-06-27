from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
import re


def phone_validator(value):
    if not re.match(r'^(01[0169]{1}-[\d+]{3,4}-[\d+]{4})$', value):
        raise ValidationError(_('핸드폰 번호를 정확히 입력해 주세요.'))


def student_no_validator(value):
    if not re.match(r'^(20[\d+]{2}-[\d+]{5})$', value):
        raise ValidationError(_('학번을 정확히 입력해 주세요.'))


def enroll_year_validator(value):
    if not re.match(r'^(20[\d+]{2})$', str(value)):
        raise ValidationError('가입년도를 정확히 입력해 주세요.')


def snumail_validator(value):
    if not re.match(r'^(\w+@snu.ac.kr)$', value):
        raise ValidationError(_('서울대학교 이메일을 입력해 주세요.'))
