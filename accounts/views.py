from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
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


class UserActionMixin(object):
    model = User
    fields = ['rule_confirm', 'email', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic', 'join_year', 'join_semester']

    class Meta:
        abstract = True


class UserCreateView(UserActionMixin, CreateView):
    # TODO: Add Date limiting logic
    template_name = 'accounts/user_form.html'

    def form_valid(self, form):
        # TODO: Add Email verification logic
        self.object = form.save()
        # 신규 User가 생성될 때 자동으로 Active User 추가
        active_user = ActiveUser(user=self.object, active_year=self.object.join_year,
                                 active_semester=self.object.join_semester)
        active_user.save()

        return HttpResponseRedirect(self.get_success_url())


class UserDetailView(UserActionMixin, DetailView):
    pass


class UserUpdateView(UserActionMixin, UpdateView):
    template_name_suffix = '_update_form'


class ActiveUserCreateView(View):
    def get(self, request, pk):
        if not OperationScheme.can_old_register():
            return render(request, 'accounts/old_register_wait.html')
        else:
            return render(request, 'accounts/old_register.html')

    def post(self, request, pk):
        latest_os = OperationScheme.latest()
        active_user = ActiveUser(user=User.objects.get(pk=pk), active_year=latest_os.current_year,
                                 active_semester=latest_os.current_semester)
        active_user.save()
        return render(request, 'accounts/old_register_done.html')


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
