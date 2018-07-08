from django.conf.urls import url
from django.urls import path, reverse_lazy
from .views import PartnerDetailView

app_name = 'partners'

urlpatterns = [
    path('detail/<int:pk>/', PartnerDetailView.as_view(), name='detail'),
]