from django.contrib import admin
from .models import (
    OperationScheme,
    Posting,
    Instagram,
)

admin.site.register(OperationScheme)
admin.site.register(Posting)
admin.site.register(Instagram)