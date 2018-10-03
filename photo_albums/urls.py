from django.urls import path
from photo_albums.views import *

app_name = 'photo_albums'

urlpatterns = [
    path('', PhotoAlbumMainView.as_view(), name='photo-album-main'),
    path('ajax/albums/', AlbumListAjaxView.as_view(), name='albums-list'),
    path('ajax/photos/', PhotoListAjaxView.as_view(), name='photos-list'),
    path('ajax/photo/create/', photo_create_ajax_view, name='photo-create')
]
