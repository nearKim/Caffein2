from django.contrib import admin
from .models import (
    Meeting,
    CoffeeEducation,
    CoffeeMeeting,
    OfficialMeeting,
)

admin.site.register(Meeting)
admin.site.register(CoffeeMeeting)
admin.site.register(OfficialMeeting)
admin.site.register(CoffeeEducation)