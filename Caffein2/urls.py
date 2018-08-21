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
from django.contrib import admin
from django.urls import path, include

if not settings.configured:
    settings.configure('Caffein2.settings.dev', DEBUG=True)
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls', namespace='core')),
    path('comments',include('comments.urls', namespace='comments')),
    path('cafe/', include('cafe.urls', namespace='cafe')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('partners/', include('partners.urls', namespace='partners')),
    path('survey/', include('survey.urls', namespace='survey')),
    path('meetings/', include('meetings.urls', namespace='meetings')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
