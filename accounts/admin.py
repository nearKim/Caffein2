from django.contrib import admin
from .models import (
    User,
    ActiveUser
)

admin.site.register(User)
admin.site.register(ActiveUser)