from .views import CafeViewSet
from rest_framework import renderers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cafes.api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'cafes', views.CafeViewSet, basename='cafe')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]