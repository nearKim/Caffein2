from django.urls import path

from cafes.search import search_place
from .views import (
    CafeDetailView,
    CafeListView,
    CafeCreateView,
    CafeUpdateView,
    CafeSearchView
)

app_name = 'cafes'

urlpatterns = [
    path('', CafeListView.as_view(), name='cafes-list'),
    path('detail/<int:pk>', CafeDetailView.as_view(), name='cafes-detail'),
    path('create', CafeCreateView.as_view(), name='cafes-create'),
    path('update/<int:pk>', CafeUpdateView.as_view(), name='cafes-update'),
    path('search', CafeSearchView.as_view(), name='cafes-search'),

    path('ajax/search-place', search_place, name='search-place')
]
