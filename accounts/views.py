from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import (
    User,
    ActiveUser
)


class UserCreate(CreateView):
    model = User
    fields = ['rule_confirm', 'email', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic', 'join_year', 'join_semester']
    template_name = 'accounts/user_form.html'
