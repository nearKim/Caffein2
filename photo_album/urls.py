from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static

from photo_album import views
app_name = 'photo_album'

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
