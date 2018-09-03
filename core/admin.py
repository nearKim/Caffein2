from django.contrib import admin

from .models import (
    OperationScheme,
    Instagram,
    FeedPhoto
)
from comments.models import Comment

admin.site.register(OperationScheme)
admin.site.register(FeedPhoto)
admin.site.register(Instagram)

