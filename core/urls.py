from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import path, reverse_lazy

from .views import entrypoint

app_name = 'core'

urlpatterns = [
    path('', entrypoint, name='entrypoint'),
    path('home/', LoginView.as_view(template_name='index.html', ), name='index'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:index')), name='logout'),



]
