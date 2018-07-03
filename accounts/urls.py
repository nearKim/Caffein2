from django.urls import path
from .views import (
    UserCreateView,
    UserDetailView,
    UserUpdateView,
    PaymentView
)

app_name = 'accounts'

urlpatterns = [
    path('', UserCreateView.as_view(), name='register'),
    path('<int:pk>/profile/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/payment/', PaymentView.as_view(), name='payment'),
]