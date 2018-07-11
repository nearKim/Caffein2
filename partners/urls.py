from django.urls import path

from .views import (
    PartnerDetailView,
    PartnerMeetingListView,
    PartnerMeetingCreateView,
    PartnerMeetingUpdateView,
)

app_name = 'partners'

urlpatterns = [
    path('detail/<int:pk>/', PartnerDetailView.as_view(), name='detail'),
    path('meeting/list/', PartnerMeetingListView.as_view(), name='meeting-list'),
    path('meeting/create/', PartnerMeetingCreateView.as_view(), name='meeting-create'),
    path('meeting/update/<int:pk>/', PartnerMeetingUpdateView.as_view(), name='meeting-update'),
]
