# Register your models here.
from django.contrib import admin

from .models import Cafe, CafePhoto

admin.site.register(Cafe)
admin.site.register(CafePhoto)
