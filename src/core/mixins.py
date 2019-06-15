import facebook
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.db import models
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _


# Model Mixins

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


# View Mixins

# class FaceBookPostMixin:
#     def get_success_url(self):
#         url = super(FaceBookPostMixin, self).get_success_url()
#         # 그래프 API객체를 SDK를 통해 가져온다
#         graph = facebook.GraphAPI(settings.FACEBOOK_TOKEN)
#         # 그룹아이디를 이용하여 put_object를 통해 그룹에 글을 쓴다.
#         # 메세지는 상속받는 클래스의 생성자에서 각각 다르게 설정해야겠지
#         message = self.message if self.message else 'test'
#         # FIXME: 페이스북 API는 localhost를 valid link로 인정하지 않는다. Production 환경에서 실제 URL로 교체가 필요하다. Logging도 필요하다
#         # graph.put_object(FACEBOOK_GROUP_ID, "feed", message=message, link='https://{}{}'.format(Site.objects.get_current().domain, url))
#         graph.put_object(settings.FACEBOOK_GROUP_ID, "feed", message=message, link='https://www.naver.com')
#         return url
#
#     class Meta:
#         abstract = True


class StaffRequiredMixin(AccessMixin):
    """현재 유저가 운영진이 아니라면 403을 반환한다"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif not request.user.is_staff:
            raise PermissionDenied
        else:
            return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class StaffOrMeRequiredMixin(AccessMixin):
    """운영진이거나 유저가 해당 객체 자신이 아니면 403을 반환한다"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.get_object() != request.user and not request.user.is_staff:
            raise PermissionDenied
        else:
            return super(StaffOrMeRequiredMixin, self).dispatch(request, *args, **kwargs)


class ValidAuthorRequiredMixin(AccessMixin):
    """해당 객체의 author가 운영진이거나 객체의 author가 아니면 403을 반환한다"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif self.get_object().author != request.user and not request.user.is_staff:
            raise PermissionDenied
        else:
            return super(ValidAuthorRequiredMixin, self).dispatch(request, *args, **kwargs)


# Admin mixins
class StaffRequiredAdminMixin(object):
    # FIXME: 이 mixin을 통해 수정 및 삭제 권한을 부여하려 했었지만 delete는 permission이 주어지지 않았다.
    # FIXME: 지금은 User based로 permission을 부여했기 때문에 이 mixin이 불필요하다.

    def check_perm(self, user_obj):
        if not user_obj.is_active or user_obj.is_anonymous:
            return False
        if user_obj.is_superuser or user_obj.is_staff:
            return True
        return False

    def has_module_permission(self, request):
        return self.check_perm(request.user)

    def has_add_permission(self, request):
        return self.check_perm(request.user)

    def has_change_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_delete_permission(self, request, obj=None):
        return self.check_perm(request.user)
