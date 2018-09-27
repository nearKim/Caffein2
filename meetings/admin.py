from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline

from comments.models import Comment
from core.mixins import StaffRequiredAdminMixin
from .models import (
    CoffeeEducation,
    CoffeeMeeting,
    OfficialMeeting)
from core.models import Meeting, MeetingPhoto


class MeetingPhotoInline(StaffRequiredAdminMixin, TabularInline):
    model = MeetingPhoto


class MeetingCommentInline(StaffRequiredAdminMixin, TabularInline):
    model = Comment
    # 혼선방지를 위해 instagram은 제외함
    exclude = ('instagram',)


@admin.register(CoffeeMeeting)
class CoffeeMeetingAdmin(StaffRequiredAdminMixin, ModelAdmin):
    list_filter = ('cafe',)
    search_fields = ('cafe__name',)
    inlines = (MeetingCommentInline, MeetingPhotoInline,)


@admin.register(OfficialMeeting)
class OfficialMeetingAdmin(StaffRequiredAdminMixin, ModelAdmin):
    list_filter = ('category',)
    readonly_fields = ('location', 'mapx', 'mapy',)
    inlines = (MeetingCommentInline, MeetingPhotoInline,)


@admin.register(CoffeeEducation)
class CoffeeEducationAdmin(StaffRequiredAdminMixin, ModelAdmin):
    list_filter = ('category', 'difficulty')
    readonly_fields = ('location', 'mapx', 'mapy',)
    inlines = (MeetingCommentInline, MeetingPhotoInline,)
