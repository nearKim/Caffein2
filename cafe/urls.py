from django.urls import path

from cafe.search import search_place
from .views import CafeListView, CafeDetailView, index, CafeCreateView, CafeDeleteView, CafeUpdateView

app_name = 'cafe'

urlpatterns = [
    path('', index, name='index'),
    path('list', CafeListView.as_view(), name='cafe-list'),
    path('detail/<int:pk>', CafeDetailView.as_view(), name='cafe-detail'),
    path('create', CafeCreateView.as_view(), name='cafe-create'),
    path('update/<int:pk>', CafeUpdateView.as_view(), name='cafe-update'),
    path('delete/<int:pk>', CafeDeleteView.as_view(), name='cafe-delete'),
    path('search', search_place, name='search-place')
]
