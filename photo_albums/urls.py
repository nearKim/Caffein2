from django.urls import path
from photo_albums.views import *

app_name = 'photo_albums'

urlpatterns = [
    path('', PhotoAlbumMainView.as_view(), name='photo-album-main'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),

    path('ajax/albums/', AlbumListAjaxView.as_view(), name='albums-list'),
    path('ajax/photos/', PhotoListAjaxView.as_view(), name='photos-list'),
    path('ajax/photo/create/', photo_create_ajax_view, name='photo-create'),
    path('ajax/photo/desc-update/', photo_description_update_ajax_view, name='photo-desc-update'),
    path('ajax/album/create/', album_create_ajax_view, name='album-create'),
]
