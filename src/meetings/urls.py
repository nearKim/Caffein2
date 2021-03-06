from django.urls import path

from .views import (
    OfficialAndEducationListView,
    OfficialMeetingCreateView,
    OfficialMeetingUpdateView,
    OfficialMeetingDetailView,
    OfficialMeetingListView,

    CoffeeEducationCreateView,
    CoffeeEducationUpdateView,
    CoffeeEducationListView,
    CoffeeEducationDetailView,

    CoffeeMeetingCreateView,
    CoffeeMeetingDetailView,
    CoffeeMeetingListView,
    CoffeeMeetingUserListView,
    CoffeeMeetingUpdateView,

    participate_meeting,
    delete_meeting,
)

app_name = 'meetings'

urlpatterns = [
    path('', OfficialAndEducationListView.as_view(), name='meetings-list'),
    path('official/create/', OfficialMeetingCreateView.as_view(), name='official-create'),
    path('official/update/<int:pk>/', OfficialMeetingUpdateView.as_view(), name='official-update'),
    path('official/', OfficialMeetingListView.as_view(), name='official-list'),
    path('official/<int:pk>/', OfficialMeetingDetailView.as_view(), name='official-detail'),

    path('education/create/', CoffeeEducationCreateView.as_view(), name='education-create'),
    path('education/update/<int:pk>/', CoffeeEducationUpdateView.as_view(), name='education-update'),
    path('education/<int:pk>/', CoffeeEducationDetailView.as_view(), name='education-detail'),
    path('education/', CoffeeEducationListView.as_view(), name='education-list'),

    path('coffee-meeting/create/<int:pk>', CoffeeMeetingCreateView.as_view(), name='coffee-meeting-create'),
    path('coffee-meeting/update/<int:pk>', CoffeeMeetingUpdateView.as_view(), name='coffee-meeting-update'),
    path('coffee-meeting/<int:pk>', CoffeeMeetingDetailView.as_view(), name='coffee-meeting-detail'),
    path('coffee-meeting/', CoffeeMeetingListView.as_view(), name='coffee-meeting-list'),
    path('coffee-meeting/user/', CoffeeMeetingUserListView.as_view(), name='coffee-meeting-user-list'),

    path('participate/<int:pk>/', participate_meeting, name='participate'),
    path('delete-meeting/<int:pk>', delete_meeting, name='delete-meeting'),
]
