from django.urls import path

from photo_albums.views import (
    PhotoAlbumMainView,
    AlbumDetailView,
    PhotoDetailView,
    AlbumDeleteView,
    PhotoDeleteView,
    AlbumUpdateView,
    PhotoUpdateView,
    AlbumListAjaxView,
    PhotoListAjaxView,
    photo_create_ajax_view,
    photo_description_update_ajax_view,
    album_create_ajax_view
)

app_name = 'photo_albums'

urlpatterns = [
    path('', PhotoAlbumMainView.as_view(), name='photo-album-main'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('album/delete/<int:pk>/', AlbumDeleteView.as_view(), name='album-delete'),
    path('photo/delete/<int:pk>/', PhotoDeleteView.as_view(), name='photo-delete'),
    path('album/update/<int:pk>/', AlbumUpdateView.as_view(), name='album-update'),
    path('photo/update/<int:pk>/', PhotoUpdateView.as_view(), name='photo-update'),

    path('ajax/albums/', AlbumListAjaxView.as_view(), name='albums-list'),
    path('ajax/photos/', PhotoListAjaxView.as_view(), name='photos-list'),
    path('ajax/photo/create/', photo_create_ajax_view, name='photo-create'),
    path('ajax/photo/desc-update/', photo_description_update_ajax_view, name='photo-desc-update'),
    path('ajax/album/create/', album_create_ajax_view, name='album-create'),
]
