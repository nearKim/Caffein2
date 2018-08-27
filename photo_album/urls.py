from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from photo_album.views import *

app_name = 'photo_album'

urlpatterns = [
    path('clear', clear_database, name='clear_database'),
    path('basic-upload/<int:album_id>', BasicUploadView.as_view(), name='basic_upload'),
    path('progress-bar-upload', ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    path('drag-and-drop-upload/<int:album_id>', DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
    path('album', AlbumLV.as_view(), name='album_list'),
    path('album_create', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>', AlbumDV.as_view(), name='album_detail'),
    path('photo/<int:pk>', PhotoDV.as_view(), name='photo_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
