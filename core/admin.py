from django.contrib import admin

from core.mixins import StaffRequiredAdminMixin
from .models import (
    OperationScheme,
    Instagram,
    FeedPhoto
)


class OperationSchemeAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    raw_id_fields = ('boss',)


admin.site.register(OperationScheme, OperationSchemeAdmin)
admin.site.register(FeedPhoto)
admin.site.register(Instagram)
