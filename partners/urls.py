from django.urls import path

from .views import (
    PartnerDetailView,
    PartnerMeetingListView,
    PartnerMeetingCreateView,
)

app_name = 'partners'

urlpatterns = [
    path('detail/<int:pk>/', PartnerDetailView.as_view(), name='detail'),
    path('meeting-list/', PartnerMeetingListView.as_view(), name='meeting-list' ),
    path('create-meeting/', PartnerMeetingCreateView.as_view(), name='meeting-create'),
]
