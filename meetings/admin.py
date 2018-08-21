from django.contrib import admin

from .models import (
    CoffeeEducation,
    CoffeeMeeting,
    OfficialMeeting)
from core.models import Meeting, MeetingPhotos

admin.site.register(Meeting)
admin.site.register(MeetingPhotos)
admin.site.register(CoffeeMeeting)
admin.site.register(OfficialMeeting)
admin.site.register(CoffeeEducation)