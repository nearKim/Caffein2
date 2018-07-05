from django.urls import path, reverse_lazy
from .views import (
    UserCreateView,
    UserDetailView,
    UserUpdateView,
    ActiveUserCreateView,
    PaymentView
)


app_name = 'accounts'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('<int:pk>/profile/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/pay/', PaymentView.as_view(), name='payment'),
    path('<int:pk>/old-register/', ActiveUserCreateView.as_view(), name='old-register'),
]