"""Caffein2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

# if not settings.configured:
#     settings.configure('Caffein2.settings.dev', DEBUG=True)
from django.conf.urls.static import static

from core.models import OperationScheme

urlpatterns = [
    path('admin/', admin.site.urls, {'extra_context': {'os': OperationScheme.latest()}}),

    path('', include('core.urls', namespace='core')),
    path('comments', include('comments.urls', namespace='comments')),
    path('cafes/', include('cafes.urls', namespace='cafes')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('partners/', include('partners.urls', namespace='partners')),
    path('photo_albums/', include('photo_albums.urls', namespace='photo_albums')),
    path('surveys/', include('surveys.urls', namespace='surveys')),
    path('meetings/', include('meetings.urls', namespace='meetings')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)), ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
