from django.urls import path
from .views import (
    UserCreateView,
    UserDetailView,
)

app_name = 'accounts'

urlpatterns = [
    path('', UserCreateView.as_view(), name='register'),
    path('<int:pk>/profile/', UserDetailView.as_view(), name='detail'),
]