#from django.conf.urls import url, include
from django.urls import path
from .views import CafeListView, CafeDetailView
app_name = 'cafe'

urlpatterns = [
    path('', CafeListView.as_view(), name='cafe-list'),
    path('<int:pk>', CafeDetailView.as_view, name='cafe-detail')
]
