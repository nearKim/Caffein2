from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views import View
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.detail import DetailView
from .models import (
    User,
    ActiveUser
)
from core.models import OperationScheme


class UserCreateView(CreateView):
    model = User
    fields = ['rule_confirm', 'email', 'password', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic', 'join_year', 'join_semester']
    template_name = 'accounts/new_register.html'

    def dispatch(self, request, *args, **kwargs):
        # TODO: Add Email verification logic
        if not OperationScheme.can_new_register():
            return HttpResponse('아직 가입기간이 아닙니다')
        else:
            # https://stackoverflow.com/questions/5433172/how-to-redirect-on-conditions-with-class-based-views-in-django-1-3
            return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        active_user = ActiveUser(user=self.object, active_year=self.object.join_year,
                                 active_semester=self.object.join_semester)
        active_user.save()

        return HttpResponseRedirect(self.get_success_url())


class UserDetailView(DetailView):
    model = User
    fields = ['rule_confirm', 'email', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic', 'join_year', 'join_semester']


class UserUpdateView(UpdateView):
    template_name_suffix = '_update_form'
    model = User
    fields = ['rule_confirm', 'email', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic']


class ActiveUserCreateView(CreateView):
    # FIXME: Login기능 구현 후 request에 user 객체를 담아 활용

    model = ActiveUser
    fields = []

    def dispatch(self, request, *args, **kwargs):
        if not OperationScheme.can_old_register():
            return HttpResponse('아직 가입기간이 아닙니다.')
        else:
            return super(ActiveUserCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form, pk):
        latest_os = OperationScheme.latest()
        user = self.request.user
        form.instance.user = user
        form.instance.active_year = latest_os.current_year
        form.instance.active_semester = latest_os.current_semester
        return super(ActiveUserCreateView, self).form_valid(form)


class PaymentView(View):
    latest_os = OperationScheme.latest()

    def get(self, request, pk):
        # FIXME: Retrieval of an ActiveUser based on user pk might return multiple rows. Add latest logic.
        active_user = ActiveUser.objects.get(user__pk=pk)
        print(active_user.is_new)
        if active_user.is_new:
            return render(request, 'accounts/new_pay.html', context={'active_user': active_user, 'os': self.latest_os})
        else:
            return render(request, 'accounts/old_pay.html', context={'active_user': active_user, 'os': self.latest_os})
