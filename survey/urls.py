'''
from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
'''
#from rest_framework import routers
from django.conf.urls import url, include

from .views import view_form, FormListView, FormCreate, delete_form
app_name = 'survey'
'''
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)
'''
urlpatterns = [
    # url(r'^home/', home),
    url(r'^home/', FormListView.as_view(), name="form-list"),
    url(r'^create/', FormCreate.as_view(), name="form-create"),
    url(r'^view_form/(?P<pk>\d+)/(?P<user_id>\d+)$', view_form, name="view-form"),
    url(r'^delete_form/(?P<pk>\d+)$', delete_form, name="delete-form")
    # url(r'^api/', include(router.urls)),
]
