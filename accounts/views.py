from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from .models import (
    User,
    ActiveUser
)


class UserCreateView(CreateView):
    model = User
    fields = ['rule_confirm', 'email', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic', 'join_year', 'join_semester']
    template_name = 'accounts/user_form.html'

    def form_valid(self, form):
        # TODO: Add Email verification logic
        self.object = form.save()
        active_user = ActiveUser(user=self.object, active_year=self.object.join_year,
                                 active_semester=self.object.join_semester)
        active_user.save()

        return HttpResponseRedirect(self.get_success_url())


class UserDetailView(DetailView):
    model = User
