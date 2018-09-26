from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.template.response import TemplateResponse
from django.urls import path

from accounts.models import ActiveUser
from comments.models import Comment
from core.mixins import StaffRequiredAdminMixin
from core.models import FeedPhoto, OperationScheme
from .models import (
    Partner,
    PartnerMeeting
)


@admin.register(Partner)
class PartnerAdmin(StaffRequiredAdminMixin, ModelAdmin):
    list_filter = ('partner_year', 'partner_semester')
    search_fields = ('up_partner', 'down_partner_1', 'down_partner_2', 'down_partner_3')
    ordering = ('-partner_year', '-partner_semester')


class FeedPhotoInline(StaffRequiredAdminMixin, TabularInline):
    model = FeedPhoto


class FeedCommentInline(StaffRequiredAdminMixin, TabularInline):
    model = Comment
    # 혼선방지를 위해 meeting은 제외함
    exclude = ('meeting',)


@admin.register(PartnerMeeting)
class PartnerMeetingAdmin(StaffRequiredAdminMixin, ModelAdmin):
    inlines = (FeedPhotoInline, FeedCommentInline)

