from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class TimeStampedMixin(models.Model):
    """TimeStamp가 필요한 모든 모델에 사용되는 Mixin"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Instable(TimeStampedMixin):
    """ActiveUser에 의한 포스팅 중 내용 및 사진만 포함하는 포스팅(Instagram 형식)"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('작성자'))
    content = models.TextField(_('내용'), max_length=1000)

    class Meta:
        abstract = True


class Postable(Instable):
    """ActiveUser에 의한 포스팅 중 내용, 사진 및 제목까지 모두 포함하는 포스팅(일반 Blog 형식)"""
    title = models.CharField(_('제목'), max_length=20, blank=True)

    class Meta:
        abstract = True
