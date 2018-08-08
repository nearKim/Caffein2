from django.contrib import admin

from .models import (
    OperationScheme,
    Instagram,
    FeedPhotos,
    Comment
)

admin.site.register(OperationScheme)
admin.site.register(FeedPhotos)
admin.site.register(Instagram)
admin.site.register(Comment)
