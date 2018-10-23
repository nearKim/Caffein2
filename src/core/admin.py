from django.contrib import admin

from core.mixins import StaffRequiredAdminMixin
from .models import (
    OperationScheme,
    Instagram,
    FeedPhoto,
)


class OperationSchemeAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    raw_id_fields = ('boss',)


class FeedPhotoInline(StaffRequiredAdminMixin, admin.TabularInline):
    model = FeedPhoto


@admin.register(Instagram)
class FeedAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    inlines = (FeedPhotoInline,)


admin.site.register(OperationScheme, OperationSchemeAdmin)
# admin.site.register(Instagram)
# admin.site.register(FeedPhoto)
