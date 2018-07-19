from django.contrib import admin

from .models import (
    Meeting,
    CoffeeEducation,
    CoffeeMeeting,
    OfficialMeeting,
    MeetingPhotos)

admin.site.register(Meeting)
admin.site.register(MeetingPhotos)
admin.site.register(CoffeeMeeting)
admin.site.register(OfficialMeeting)
admin.site.register(CoffeeEducation)