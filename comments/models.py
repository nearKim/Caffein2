from django.db import models

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from core.mixins import Postable


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        obj_id = instance.id
        qs = super(CommentManager, self).filter(id=obj_id)
        return qs


class Comment(Postable):
    instagram = models.ForeignKey('core.Instagram', default=None, null=True, blank=True, related_name='comments',
                                  on_delete=models.CASCADE)
    meeting = models.ForeignKey('core.Meeting', default=None, null=True, blank=True, related_name='comments',
                                on_delete=models.CASCADE)
    objects = CommentManager()

    class Meta:
        verbose_name = _('댓글')
        verbose_name_plural = _('댓글')

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        if self.instagram:
            # partner:meeting-list로 redirect
            return reverse('partners:meeting-list')
        elif self.meeting:
            # downcast후 각 클래스의 get_absolute_url로 redirect
            return self.meeting.cast().get_absolute_url()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.instagram is None and self.meeting is None:
            # Don't save
            return
        super(Comment, self).save()