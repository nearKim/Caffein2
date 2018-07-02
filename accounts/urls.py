from django.urls import path
from .views import (
    UserCreate
)

app_name = 'accounts'

urlpatterns = [
    path('', UserCreate.as_view(), name='register'),
]