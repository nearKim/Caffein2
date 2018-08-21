from django.contrib import admin

from .models import (
    OperationScheme,
    Instagram,
    FeedPhotos
)
from comments.models import Comment

admin.site.register(OperationScheme)
admin.site.register(FeedPhotos)
admin.site.register(Instagram)

