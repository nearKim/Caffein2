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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('작성자'))
    content = models.TextField(_('내용'), max_length=1000)

    # TODO: Implement 'likes' field
    # https://devdoggo.netlify.com/post/python/django/counter/

    class Meta:
        abstract = True
