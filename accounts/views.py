from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import six
from django.utils.timezone import now

from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from .models import (
    User,
    ActiveUser
)
from core.models import OperationScheme
from .forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # TODO: Link to the survey app.
        return HttpResponse(_('이메일 계정이 확인되었습니다. 이제 로그인 하실 수 있습니다.'))
    else:
        return HttpResponse(_('Activation Link invalid. Try again.'))


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


class UserCreateView(CreateView):
    model = User
    fields = ['rule_confirm', 'email', 'password', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic', 'join_year', 'join_semester']
    template_name = 'accounts/new_register.html'

    def dispatch(self, request, *args, **kwargs):
        # TODO: Add Email verification logic
        # FIXME: not!
        if OperationScheme.can_new_register():
            return HttpResponse('아직 가입기간이 아닙니다')
        else:
            # https://stackoverflow.com/questions/5433172/how-to-redirect-on-conditions-with-class-based-views-in-django-1-3
            return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = _('[서울대학교 커피동아리 카페인] 가입인증 메일입니다')
        mail_body = render_to_string('accounts/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, mail_body, to=[to_email])
        email.send()
        return HttpResponse(_('가입인증 이메일이 보내졌습니다. 이메일을 확인해주세요.'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    fields = ['rule_confirm', 'email', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic', 'join_year', 'join_semester']


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = '_update_form'
    model = User
    fields = ['rule_confirm', 'email', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic']


class ActiveUserCreateView(LoginRequiredMixin, CreateView):
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

    def get(self, request, pk):
        # FIXME: Retrieval of an ActiveUser based on user pk might return multiple rows. Add latest logic.
        active_user = ActiveUser.objects.get(user__pk=pk)
        latest_os = OperationScheme.latest()
        pay = latest_os.new_pay if active_user.is_new else latest_os.old_pay

        return render(request, 'accounts/now_pay.html',
                      context={'active_user': active_user, 'os': latest_os, 'pay': pay})
