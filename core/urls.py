from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import path, reverse_lazy

from .views import (
    index,
    CommentCreateView,
    CommentDeleteView,
    CommentListView,
    CommentUpdateView,
    CommentDetailView
)

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:login')), name='logout'),

    path('comment/create/<int:insta_id>/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/list/', CommentListView.as_view(), name='comment-list'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),

]
