from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from core.models import OperationScheme


def meeting_coffee_validator(value):
    latest_os = OperationScheme.latest()
    if value > latest_os.limit_coffee:
        raise ValidationError(_('일일 제한 커모 횟수인 {}회 이하로 입력해주세요.'.format(latest_os.limit_coffee)))


def meeting_eat_validator(value):
    latest_os = OperationScheme.latest()
    if value > latest_os.limit_eat:
        raise ValidationError(_('일일 제한 밥모 횟수인 {}회 이하로 입력해주세요.'.format(latest_os.limit_eat)))