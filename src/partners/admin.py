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
    PartnerMeeting,
    CoffeeMeetingFeed
)


class FeedCommentInline(StaffRequiredAdminMixin, TabularInline):
    model = Comment
    # 혼선방지를 위해 meeting은 제외함
    exclude = ('meeting',)


@admin.register(Partner)
class PartnerAdmin(StaffRequiredAdminMixin, ModelAdmin):
    list_display = ('__str__', 'score', 'up_partner', 'down_partner_1', 'down_partner_2',
                    'down_partner_3')
    list_filter = ('partner_year', 'partner_semester')
    search_fields = (
        'up_partner__user__name', 'down_partner_1__user__name', 'down_partner_2__user__name',
        'down_partner_3__user__name')
    ordering = ('-partner_year', '-partner_semester', '-score')
    list_select_related = ('up_partner__user', 'down_partner_1__user', 'down_partner_2__user', 'down_partner_3__user',)


@admin.register(PartnerMeeting)
class PartnerMeetingAdmin(StaffRequiredAdminMixin, ModelAdmin):
    inlines = (FeedPhotoInline, FeedCommentInline)
    list_select_related = ('partner__up_partner', 'partner__down_partner_1', 'partner__down_partner_2',
                           'partner__down_partner_3',)


@admin.register(CoffeeMeetingFeed)
class CoffeeMeetingFeedAdmin(StaffRequiredAdminMixin, ModelAdmin):
    inlines = (FeedPhotoInline, FeedCommentInline)
    list_select_related = ('coffee_meeting__cafe', 'author')
