from django.conf.urls import url
from django.urls import path, reverse_lazy
from .views import (
    UserCreateView,
    activate,
    UserDetailView,
    UserUpdateView,
    ActiveUserCreateView,
    PaymentView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/pay/', PaymentView.as_view(), name='payment'),
    path('<int:pk>/old-register/', ActiveUserCreateView.as_view(), name='old-register'),
]
