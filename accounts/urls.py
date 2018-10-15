from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import (
    UserCreateView,
    activate,
    UserDetailView,
    UserUpdateView,
    ActiveUserCreateView,
    PaymentView,
    export_users_excel,
    old_register_done,
    load_departments)

app_name = 'accounts'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    path('change-password/',
         auth_views.PasswordChangeView.as_view(template_name="accounts/registration/password_change_form.html",
                                               success_url=reverse_lazy('accounts:password-change-done')),
         name='password-change'),
    path('change-password/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="accounts/registration/password_change_done.html"),
         name='password-change-done'),

    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/pay/', PaymentView.as_view(), name='payment'),
    path('<int:pk>/old-register/', ActiveUserCreateView.as_view(), name='old-register'),
    path('export/<int:category>/', export_users_excel, name='export-users-excel'),
    #path('export/old/', export_old_users_excel, name='export-old-users-excel'),
    #path('export/new/', export_new_users_excel, name='export-new-users-excel'),
    path('old-register/done/', old_register_done, name='old-register-done'),

    path('ajax/load-departments/', load_departments, name='ajax-load-departments'),
]
