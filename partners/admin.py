from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.template.response import TemplateResponse
from django.urls import path

from accounts.models import ActiveUser
from comments.models import Comment
from core.models import FeedPhoto, OperationScheme
from .models import (
    Partner,
    PartnerMeeting
)


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    list_filter = ('partner_year', 'partner_semester')
    search_fields = ('up_partner', 'down_partner_1', 'down_partner_2', 'down_partner_3')
    ordering = ('-partner_year', '-partner_semester')


class FeedPhotoInline(TabularInline):
    model = FeedPhoto


class FeedCommentInline(TabularInline):
    model = Comment
    # 혼선방지를 위해 meeting은 제외함
    exclude = ('meeting',)


@admin.register(PartnerMeeting)
class PartnerMeetingAdmin(ModelAdmin):
    inlines = (FeedPhotoInline, FeedCommentInline)

