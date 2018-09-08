from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline

from comments.models import Comment
from .models import (
    CoffeeEducation,
    CoffeeMeeting,
    OfficialMeeting)
from core.models import Meeting, MeetingPhoto


class MeetingPhotoInline(TabularInline):
    model = MeetingPhoto


class MeetingCommentInline(TabularInline):
    model = Comment
    # 혼선방지를 위해 instagram은 제외함
    exclude = ('instagram',)


@admin.register(CoffeeMeeting)
class CoffeeMeetingAdmin(ModelAdmin):
    list_filter = ('cafe',)
    inlines = (MeetingCommentInline, MeetingPhotoInline,)


@admin.register(OfficialMeeting)
class OfficialMeetingAdmin(ModelAdmin):
    list_filter = ('category',)
    readonly_fields = ('location', 'mapx', 'mapy',)
    inlines = (MeetingCommentInline, MeetingPhotoInline,)


@admin.register(CoffeeEducation)
class CoffeeEducationAdmin(ModelAdmin):
    list_filter = ('category', 'difficulty')
    readonly_fields = ('location', 'mapx', 'mapy',)
    inlines = (MeetingCommentInline, MeetingPhotoInline,)
