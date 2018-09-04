# Register your models here.
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Cafe, CafePhoto


class CafePhotoInline(admin.TabularInline):
    model = CafePhoto


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('uploader', 'name', 'address', 'description', 'phone', 'price')}),
        (_('커피 정보'), {'fields': ('machine', 'grinder')}),
        (_('운영 정보'), {'fields': ('from_time', 'to_time', 'closed_day', 'closed_holiday')}),
        (_('기타 정보'), {'fields': ('link', 'road_address', 'mapx', 'mapy')})
    )
    readonly_fields = ('road_address','mapx', 'mapy')
    search_fields = ('name', 'address', 'road_address', 'description', 'phone')
    list_filter = ('closed_day', 'price')
    inlines = (CafePhotoInline,)
