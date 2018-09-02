from django.urls import path
from photo_albums.views import *

app_name = 'photo_albums'

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    path('album/<int:pk>', AlbumDetailView.as_view(), name='album_detail'),
    path('album_create', AlbumCreateView.as_view(), name='album_create'),
    path('album_edit/<int:album_id>', AlbumEditView.as_view(), name='album_edit'),
    path('clear/<int:pk>', clear_database, name='clear_database'),
    path('delete-photo/<int:pk>', delete_photo, name='delete_photo'),
    path('delete-photo-to-detail/<int:pk>', delete_photo_to_album_detail, name='delete_photo_to_detail'),
    path('photo/<int:pk>', PhotoDetailView.as_view(), name='photo_detail'),
]