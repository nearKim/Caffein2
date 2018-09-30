from django.urls import path

from comments.views import (
    InstagramCommentCreateView,
    MeetingCommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    CommentCreateAjaxView
)

app_name = 'comments'

urlpatterns = [
    path('comment/create/<int:pk>/<slug:to>/', CommentCreateAjaxView.as_view(), name='comment-create'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    # path('comment/create/instagram/<int:pk>/', InstagramCommentCreateView.as_view(), name='instagram-comment-create'),
    # path('comment/create/meeting/<int:pk>/', MeetingCommentCreateView.as_view(), name='meeting-comment-create'),
]
