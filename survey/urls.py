from django.conf.urls import url, include

from .views import view_form, new_view_form, FormListView, FormCreate, delete_form, list_form, change_form_state
app_name = 'survey'

urlpatterns = [
    url(r'^home/', FormListView.as_view(), name="form-list"),
    #url(r'^join/', NewFormListView.as_view(), name="new-form-list"),
    url(r'^create/', FormCreate.as_view(), name="form-create"),
    url(r'^view_form/(?P<pk>\d+)/(?P<user_id>\d+)$', view_form, name="view-form"),
    url(r'^join_form/(?P<user_id>\d+)$', new_view_form, name="new-view-form"),
    url(r'^list_form/(?P<pk>\d+)$', list_form, name="list-form"),
    url(r'^delete_form/(?P<pk>\d+)$', delete_form, name="delete-form"),
    url(r'^change_form_state/(?P<pk>\d+)$', change_form_state, name="change-form-state"),
]
