from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Postable(TimeStampedMixin):
    """Mixin for models with only one content text field"""
    content = models.TextField(_('내용'), max_length=1000)

    class Meta:
        abstract = True

