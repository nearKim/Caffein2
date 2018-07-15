from django.conf.urls import url, include

from .views import view_form, FormListView, FormCreate, delete_form, list_form, change_form_state#, check_user, check_answer
app_name = 'survey'

urlpatterns = [
    url(r'^home/', FormListView.as_view(), name="form-list"),
    url(r'^create/', FormCreate.as_view(), name="form-create"),
    url(r'^view_form/(?P<pk>\d+)/(?P<user_id>\d+)$', view_form, name="view-form"),
    url(r'^list_form/(?P<pk>\d+)$', list_form, name="list-form"),
    url(r'^delete_form/(?P<pk>\d+)$', delete_form, name="delete-form"),
    url(r'^change_form_state/(?P<pk>\d+)$', change_form_state, name="change-form-state"),
    #url(r'^check_user/(?P<form_id>\d+)/(?P<user_id>\d+)$', check_user, name="check_user"),
    #url(r'^check_answer/(?P<form_id>\d+)/(?P<user_id>\d+)$', check_answer, name="check_answer"),
]
