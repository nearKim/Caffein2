from django.conf.urls import url

from .views import survey_fill, survey_fill_new, FormListView, FormCreate, delete_form, survey_result, change_form_state

app_name = 'survey'

urlpatterns = [
    url(r'^home/', FormListView.as_view(), name="survey-list"),
    url(r'^create/', FormCreate.as_view(), name="survey-create"),
    url(r'^fill/(?P<pk>\d+)/(?P<user_id>\d+)$', survey_fill, name="survey-fill"),
    url(r'^join_form/(?P<user_id>\d+)$', survey_fill_new, name="survey-fill-new"),
    url(r'^result/(?P<pk>\d+)$', survey_result, name="survey-result"),
    url(r'^delete_form/(?P<pk>\d+)$', delete_form, name="delete-form"),
    url(r'^change_form_state/(?P<pk>\d+)$', change_form_state, name="change-form-state"),
]
