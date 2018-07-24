from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import six
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from core.models import OperationScheme
from .models import ActiveUser


def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # user.is_active = True
        # user.save()
        # login(request, user)
        messages.info(request, _('서울대계정 이메일이 확인되었습니다. 가입설문으로 이동합니다.'))
        return redirect('survey:new-view-form', user_id=uid)
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
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'accounts/new_register.html'

    def dispatch(self, request, *args, **kwargs):
        if not OperationScheme.can_new_register():
            return render(request, 'accounts/cannot_register.html',
                          context={'user': request.user, 'os': OperationScheme.latest()})
        else:
            # https://stackoverflow.com/questions/5433172/how-to-redirect-on-conditions-with-class-based-views-in-django-1-3
            return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['os'] = OperationScheme.latest()
        return context

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
    model = get_user_model()
    fields = ['rule_confirm', 'email', 'name', 'phone', 'student_no', 'college', 'department', 'category',
              'profile_pic', 'join_year', 'join_semester']


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = '_update_form'
    model = get_user_model()
    form_class = CustomUserChangeForm


class ActiveUserCreateView(LoginRequiredMixin, CreateView):
    model = ActiveUser
    fields = []
    template_name = 'accounts/old_register.html'

    def dispatch(self, request, *args, **kwargs):
        if not OperationScheme.can_old_register():
            return render(request, 'accounts/cannot_register.html',
                          context={'user': request.user, 'os': OperationScheme.latest()})
        else:
            return super(ActiveUserCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        latest_os = OperationScheme.latest()
        user = self.request.user
        current_year, current_semester = latest_os.current_year, latest_os.current_semester
        form.instance.user = user
        form.instance.active_year = current_year
        form.instance.active_semester = current_semester
        if ActiveUser(user=user, active_year=current_year, active_semester=current_semester):
            messages.error(self.request, _('이미 가입신청 하셨습니다.'))
            return self.form_invalid(form)
        else:
            return super(ActiveUserCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ActiveUserCreateView, self).get_context_data(**kwargs)
        context['os'] = OperationScheme.latest()
        return context

    def get_success_url(self):
        return reverse('accounts:old-register-done')


def old_register_done(request):
    if request.method == 'GET':
        return render(request, 'accounts/old_register_done.html', context={'user': request.user})


class PaymentView(View):

    def get(self, request, pk):
        active_user = ActiveUser.objects.get(user__pk=pk)
        latest_os = OperationScheme.latest()
        pay = latest_os.new_pay if active_user.is_new else latest_os.old_pay

        return render(request, 'accounts/now_pay.html',
                      context={'active_user': active_user, 'os': latest_os, 'pay': pay})
