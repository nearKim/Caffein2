from django.contrib import admin

from .models import (
    CoffeeEducation,
    CoffeeMeeting,
    OfficialMeeting)
from core.models import Meeting, MeetingPhoto

admin.site.register(Meeting)
admin.site.register(MeetingPhoto)
admin.site.register(CoffeeMeeting)
admin.site.register(OfficialMeeting)
admin.site.register(CoffeeEducation)