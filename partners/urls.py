from django.urls import path

from .views import (
    PartnerDetailView,
    PartnerMeetingCreateView,
)

app_name = 'partners'

urlpatterns = [
    path('detail/<int:pk>/', PartnerDetailView.as_view(), name='detail'),
    path('create-meeting/', PartnerMeetingCreateView.as_view(), name='partnermeeting-create'),
]
