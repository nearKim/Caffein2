from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, sensitive_post_parameters_m
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from core.models import OperationScheme
from partners.models import Partner
from .models import (
    ActiveUser
)

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    view_on_site = False

    list_display = ('email', 'name', 'phone', 'student_no', 'college',
                    'department', 'category', 'rule_confirm', 'survey_done', 'is_new')
    list_filter = ('join_year', 'join_semester', 'survey_done', 'college', 'category')
    list_per_page = 200
    readonly_fields = ('survey_done', 'rule_confirm')
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
    ordering = ('-date_joined',)
    actions = ['invalidate_user', 'activate_and_add_active', ]

    def is_new(self, obj):
        latest_os = OperationScheme.latest()
        if (obj.join_year, obj.join_semester) == (latest_os.current_year, latest_os.current_semester):
            return True
        else:
            return False

    is_new.boolean = True

    def activate_and_add_active(self, request, queryset):
        """신규회원 가입시 설문도 작성하고 가입비도 납부했을 경우 운영자가 확인하여 로그인활성화 및 활동회원으로 추가한다."""
        latest_os = OperationScheme.latest()
        queryset.update(is_active=True)
        for q in queryset:
            # 만일 현재 사용자가 신입회원이 아닌경우 잘못 체크된 경우이므로 에러와 함께 활동회원을 만들면 안된다.
            if not (q.join_year, q.join_semester) == (latest_os.current_year, latest_os.current_semester):
                messages.error(request, q.__str__() + ' 회원은 신규회원이 아닙니다!! 다시 확인해주세요!')
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

    is_new.short_description = _('신입 여부')
    activate_and_add_active.short_description = _('신규회원으로 확정!')
    invalidate_user.short_description = _('비활성화')


@admin.register(ActiveUser)
class ActiveUserAdmin(ModelAdmin):
    list_display = ('user', '_is_new', 'active_year', 'active_semester', 'is_paid',)
    list_filter = (
        'active_year', 'active_semester', 'is_paid', 'user__join_year', 'user__join_semester', 'user__college')
    list_editable = ('is_paid',)
    ordering = ('-active_year', '-active_semester')
    list_per_page = 150

    def get_urls(self):
        urls = super().get_urls()
        match_urls = [
            path('partner/create/', self.admin_site.admin_view(self.partner_match_view), name='partner-create'),
            path('partner/match/', self.admin_site.admin_view(self.match_partner), name='match-partner'),
        ]
        return match_urls + urls

    def partner_match_view(self, request):
        latest_os = OperationScheme.latest()
        year, semester = latest_os.current_year, latest_os.current_semester

        # 활동회원 중 이번학기 회원들을 불러온다
        active_users = ActiveUser.objects \
            .select_related('user') \
            .filter(active_year=year, active_semester=semester) \
            .order_by('user__name')

        # 이번학기 활동회원 중 신입회원과 기존회원을 분리한다
        new_actives = active_users.filter(user__join_semester=semester, user__join_year=year)
        old_actives = active_users.difference(new_actives)

        # 이번학기에 매칭된 짝지 queryset을 받아온다
        matched_users = Partner.current_activeuser_set()

        # 각 활동회원들 중 현재 매칭된 회원은 없애준다
        new_actives = new_actives.difference(matched_users)
        old_actives = old_actives.difference(matched_users).order_by('user__name')

        # 각각을 다른 context에 넣어 뿌려준다
        context = dict(
            self.admin_site.each_context(request),
            os=latest_os,
            news=new_actives,
            olds=old_actives,
        )
        return TemplateResponse(request, "admin/match_partner.html", context)

    def match_partner(self, request):
        year, semester = request.POST.get('year'), request.POST.get('semester')

        # 넘어오는 리스트는 ActiveUser의 pk들을 담고 있다
        old_list = request.POST.getlist('olds')
        new_list = request.POST.getlist('news')

        # 위,아래짝지의 수에 따라 적절한 예외처리를 해준다.
        if len(old_list) != 1:
            messages.error(request, "위짝지는 반드시 한명이어야 합니다!")
        elif not (0 < len(new_list) < 4):
            messages.error(request, "아래짝지는 1명에서 3명이어야 합니다!")
        elif len(new_list) == 1:
            Partner.objects.create(partner_year=year, partner_semester=semester,
                                   up_partner_id=old_list[0],
                                   down_partner_1_id=new_list[0],
                                   down_partner_2=None,
                                   down_partner_3=None
                                   )
            messages.success(request, "짝지가 성공적으로 매칭되었습니다")

        elif len(new_list) == 2:
            Partner.objects.create(partner_year=year, partner_semester=semester,
                                   up_partner_id=old_list[0],
                                   down_partner_1_id=new_list[0],
                                   down_partner_2_id=new_list[1],
                                   down_partner_3=None
                                   )
            messages.success(request, "짝지가 성공적으로 매칭되었습니다")
        elif len(new_list) == 3:
            Partner.objects.create(partner_year=year, partner_semester=semester,
                                   up_partner_id=old_list[0],
                                   down_partner_1_id=new_list[0],
                                   down_partner_2_id=new_list[1],
                                   down_partner_3_id=new_list[2]
                                   )
            messages.success(request, "짝지가 성공적으로 매칭되었습니다")
        # 다시 원래 화면으로 돌아가야 한다
        return redirect('admin:partner-create')
