from django.contrib import admin
from photo_albums.models import Photo, Album

admin.site.register(Album)
admin.site.register(Photo)