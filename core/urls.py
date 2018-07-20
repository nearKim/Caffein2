from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import path, reverse_lazy

from .views import (
    index,
    InstagramCommentCreateView,
    MeetingCommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
)

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:login')), name='logout'),

    path('comment/create/instagram/<int:pk>/', InstagramCommentCreateView.as_view(), name='instagram-comment-create'),
    path('comment/create/meeting/<int:pk>/', MeetingCommentCreateView.as_view(), name='meeting-comment-create'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),

]
