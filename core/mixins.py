import facebook
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

from Caffein2.settings.dev import FACEBOOK_TOKEN, FACEBOOK_GROUP_ID


class TimeStampedMixin(models.Model):
    """TimeStamp가 필요한 모든 모델에 사용되는 Mixin"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Postable(TimeStampedMixin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('작성자'))
    content = models.TextField(_('내용'), max_length=1000)

    # TODO: Implement 'likes' field
    # https://devdoggo.netlify.com/post/python/django/counter/

    class Meta:
        abstract = True


class FaceBookPostMixin:
    def get_success_url(self):
        url = super(FaceBookPostMixin, self).get_success_url()
        # 그래프 API객체를 SDK를 통해 가져온다
        graph = facebook.GraphAPI(FACEBOOK_TOKEN)
        # 그룹아이디를 이용하여 put_object를 통해 그룹에 글을 쓴다.
        # 메세지는 상속받는 클래스의 생성자에서 각각 다르게 설정해야겠지
        message = self.message if self.message else 'test'
        # FIXME: 페이스북 API는 localhost를 valid link로 인정하지 않는다. Production 환경에서 실제 URL로 교체가 필요하다. Logging도 필요하다
        # graph.put_object(FACEBOOK_GROUP_ID, "feed", message=message, link='https://{}{}'.format(Site.objects.get_current().domain, url))
        graph.put_object(FACEBOOK_GROUP_ID, "feed", message=message, link='https://www.naver.com')
        return url

    class Meta:
        abstract=True
