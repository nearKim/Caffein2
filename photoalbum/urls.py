from django.urls import path
from django.conf.urls import url, include
app_name = 'photoalbum'

urlpatterns = [
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
]
