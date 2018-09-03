from django.contrib import admin

from .models import (
    Partner,
    PartnerMeeting
)

admin.site.register(Partner)
admin.site.register(PartnerMeeting)