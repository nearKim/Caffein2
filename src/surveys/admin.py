from django.contrib import admin

from core.mixins import StaffRequiredAdminMixin
from .models import Form
from django.utils.safestring import mark_safe


class FormAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'purpose', 'opened', 'answer_num', 'result', 'owner', 'id']
    list_display_links = ['title', 'id']
    actions = ['make_opened', 'make_closed']
    ordering = ['-id', 'opened']

    # 결과창으로 가는 링크 생성
    def result(self, post):
        return mark_safe('<a href="http://localhost:8000/surveys/result/{}">응답</a>'.format(post.id))
    result.short_description = '응답보기'

    # 각 Form당 응답한 사람 수를 생성
    def answer_num(self, post):
        return mark_safe('<u>{}</u>명'.format(post.users.count()))
    answer_num.short_description = '응답자'

    # 선택한 Form의 상태를 open으로 변경
    def make_opened(self, request, queryset):
        updated_cnt = queryset.update(opened=True)
        self.message_user(request, '{}개의 Form을 열었습니다'.format(updated_cnt))
    make_opened.short_description = '지정 Form을 열기'

    # 선택한 Form의 상태를 close로 변경
    def make_closed(self, request, queryset):
        updated_cnt = queryset.update(opened=False)
        self.message_user(request, '{}개의 Form을 닫았습니다'.format(updated_cnt))
    make_closed.short_description = '지정 Form을 닫기'


# admin.site.register(Form, FormAdmin)

