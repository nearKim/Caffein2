from django.urls import path

from .views import (
    OfficialMeetingCreateView,
)

app_name = 'meetings'

urlpatterns = [
    path('create-official/', OfficialMeetingCreateView.as_view(), name='official-create'),
]
