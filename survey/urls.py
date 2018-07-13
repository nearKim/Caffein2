from django.conf.urls import url, include

from .views import view_form, FormListView, FormCreate, delete_form, list_form
app_name = 'survey'

urlpatterns = [
    url(r'^home/', FormListView.as_view(), name="form-list"),
    url(r'^create/', FormCreate.as_view(), name="form-create"),
    url(r'^view_form/(?P<pk>\d+)/(?P<user_id>\d+)$', view_form, name="view-form"),
    url(r'^list_form/(?P<pk>\d+)$', list_form, name="list-form"),
    url(r'^delete_form/(?P<pk>\d+)$', delete_form, name="delete-form")
]
