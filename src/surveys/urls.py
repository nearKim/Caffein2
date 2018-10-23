from django.urls import path
from .views import survey_fill, survey_fill_new, FormListView, FormCreate, delete_form, survey_result, change_form_state

app_name = 'surveys'

urlpatterns = [
    path('', FormListView.as_view(), name="survey-list"),
    path('create', FormCreate.as_view(), name="survey-create"),
    path('fill/<int:pk>/<int:user_id>', survey_fill, name="survey-fill"),
    path('join-form/<int:user_id>', survey_fill_new, name="survey-fill-new"),
    path('result/<int:pk>', survey_result, name="survey-result"),
    path('delete-form/<int:pk>', delete_form, name="delete-form"),
    path('change-form-state/<int:pk>', change_form_state, name="change-form-state"),
]
