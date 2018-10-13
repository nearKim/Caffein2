from django.urls import path

from .views import (
    PartnerDetailView,
    PartnerMeetingCreateView,
    PartnerMeetingUpdateView,
    PartnerMeetingDeleteView,
    FeedListView, CoffeeMeetingFeedCreateView, CoffeeMeetingFeedUpdateView, CoffeeMeetingFeedDeleteView,
    admit_or_deny_partnermeeting)

app_name = 'partners'

urlpatterns = [
    path('detail/<int:pk>/', PartnerDetailView.as_view(), name='detail'),
    # 짝모 피드에서 커모 후기까지 같이 보여준다.
    path('meeting/', FeedListView.as_view(), name='meeting-list'),
    # 짝모 관련 뷰
    path('meeting/create/', PartnerMeetingCreateView.as_view(), name='meeting-create'),
    path('meeting/update/<int:pk>/', PartnerMeetingUpdateView.as_view(), name='meeting-update'),
    path('meeting/delete/<int:pk>/', PartnerMeetingDeleteView.as_view(), name='meeting-delete'),
    path('meeting/admit-deny/<int:pk>', admit_or_deny_partnermeeting, name='meeting-admit-deny'),
    # 커모후기 관련 뷰
    path('coffee-meeting-feed/create/<int:pk>/', CoffeeMeetingFeedCreateView.as_view(), name='coffeemeeting-feed-create'),
    path('coffee-meeting-feed/update/<int:pk>/', CoffeeMeetingFeedUpdateView.as_view(), name='coffeemeeting-feed-update'),
    path('coffee-meeting-feed/delete/<int:pk>/', CoffeeMeetingFeedDeleteView.as_view(), name='coffeemeeting-feed-delete'),
]
