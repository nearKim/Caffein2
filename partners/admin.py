from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.template.response import TemplateResponse
from django.urls import path

from accounts.models import ActiveUser
from comments.models import Comment
from core.admin import FeedPhotoInline
from core.mixins import StaffRequiredAdminMixin
from core.models import FeedPhoto, OperationScheme
from .models import (
    Partner,
    PartnerMeeting
)


class FeedCommentInline(StaffRequiredAdminMixin, TabularInline):
    model = Comment
    # 혼선방지를 위해 meeting은 제외함
    exclude = ('meeting',)


@admin.register(Partner)
class PartnerAdmin(StaffRequiredAdminMixin, ModelAdmin):
    list_filter = ('partner_year', 'partner_semester')
    search_fields = (
    'up_partner__user__name', 'down_partner_1__user__name', 'down_partner_2__user__name', 'down_partner_3__user__name')
    ordering = ('-partner_year', '-partner_semester')


@admin.register(PartnerMeeting)
class PartnerMeetingAdmin(StaffRequiredAdminMixin, ModelAdmin):
    inlines = (FeedPhotoInline, FeedCommentInline)
