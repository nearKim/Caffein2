from django.urls import path

from cafe.search import search_place
from .views import (
    CafeDetailView,
    index,
    CafeCreateView,
    CafeUpdateView,
    CafeSearchView
)

app_name = 'cafe'

urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:pk>', CafeDetailView.as_view(), name='cafe-detail'),
    path('create', CafeCreateView.as_view(), name='cafe-create'),
    path('update/<int:pk>', CafeUpdateView.as_view(), name='cafe-update'),
    path('search', CafeSearchView.as_view(), name='cafe-search'),

    path('ajax/search-place', search_place, name='search-place')
]
