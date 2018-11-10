from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import path, reverse_lazy

from cafes.models import CafePhoto
from core.models import FeedPhoto
from partners.models import CoffeeMeetingFeed
from photo_albums.models import Photo
from .views import entrypoint, developer

app_name = 'core'

extra_context = {
    'staffs': get_user_model().objects.filter(is_staff=True).exclude(name='admin'),
    'feed_photo': FeedPhoto.objects.all().order_by('-created')[:3],
    'album_photo': Photo.objects.all().order_by('-created')[:3],
    'cafe_photo': CafePhoto.objects.all().order_by('-created')[:3]
}
urlpatterns = [
    path('', LoginView.as_view(template_name='index.html',
                               redirect_authenticated_user=True,
                               extra_context=extra_context), name='index'),
    path('home/', entrypoint, name='entrypoint'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:index')), name='logout'),
    path('developers/', developer, name='developers')

]
