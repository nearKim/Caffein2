from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import path, reverse_lazy

from .views import logged_in

app_name = 'core'

urlpatterns = [
    path('', LoginView.as_view(template_name='index.html', ), name='index'),
    path('index/', logged_in, name='logged-in'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:index')), name='logout'),



]
