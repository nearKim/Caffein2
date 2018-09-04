from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from core.models import OperationScheme
from .models import (
    ActiveUser
)

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'name', 'phone', 'student_no', 'college',
                    'department', 'category')
    list_filter = ('join_year', 'join_semester', 'survey_done', 'college', 'category')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('개인정보'), {'fields': ('name', 'phone', 'profile_pic')}),
        (_('학적정보'), {'fields': ('student_no', 'college', 'department', 'category')}),
        (_('권한'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('추가정보'), {'fields': ('rule_confirm', 'survey_done')}),
        (_('중요 날짜'), {'fields': ('join_year', 'join_semester', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
        (_('개인정보'), {'fields': ('name', 'phone', 'profile_pic')}),
        (_('학적정보'), {'fields': ('student_no', 'college', 'department', 'category')}),
        (_('권한'), {'fields': ('is_active', 'is_staff')}),
        (_('추가정보'), {'fields': ('rule_confirm', 'survey_done')}),
        (_('중요 날짜'), {'fields': ('join_year', 'join_semester')})
    )
    search_fields = ('email',)
    ordering = ('date_joined',)
    actions = ['activate_and_add_active']

    def activate_and_add_active(self, request, queryset):
        """신규회원 가입시 설문도 작성하고 가입비도 납부했을 경우 운영자가 확인하여 로그인활성화 및 활동회원으로 추가한다."""
        latest_os = OperationScheme.latest()
        queryset.update(is_active=True)
        for q in queryset:
            # 만일 현재 사용자가 신입회원이 아닌경우 잘못 체크된 경우이므로 에러와 함께 활동회원을 만들면 안된다.
            if not (q.join_year == latest_os.current_year and q.join_semester == latest_os.current_semester):
                self.message_user(request, q.__str__() + ' 회원은 신규회원이 아닙니다!! 다시 확인해주세요!', level=messages.WARNING)
                continue

            ActiveUser.objects.create(user=q,
                                      active_year=latest_os.current_year,
                                      active_semester=latest_os.current_semester,
                                      is_paid=True)
            # 4명까지는 알림창을 띄워주자
            if queryset.count() < 5:
                self.message_user(request, q.__str__() + '이/가 활동회원으로 등록되었습니다.')
        if queryset.count() >= 5:
            self.message_user(request, str(queryset.count()) + "명의 사용자가 활동회원으로 등록되었습니다.")

    def invalidate_user(self, request, queryset):
        """회원의 로그인 권한을 빼앗는다"""
        queryset.update(is_active=False)
        self.message_user(request, str(queryset.count()) + "명의 사용자가 비활성화 되었습니다.")

    activate_and_add_active.short_description = _('신규회원으로 확정!')
    invalidate_user.short_description = _('비활성화')


@admin.register(ActiveUser)
class ActiveUserAdmin(ModelAdmin):
    list_display = ('user', 'active_year', 'active_semester', 'is_paid')
    list_filter = (
        'active_year', 'active_semester', 'is_paid', 'user__join_year', 'user__join_semester', 'user__college')

# Now register the new UserAdmin...
