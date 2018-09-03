from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField)
from django.utils.translation import ugettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('비밀번호가 일치하지 않습니다.')
    }
    password1 = forms.CharField(
        label=_("비밀번호"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("비밀번호 확인"),
        widget=forms.PasswordInput,
        help_text=_("확인을 위해 비밀번호를 다시한번 입력해주세요."),
    )

    class Meta:
        model = get_user_model()
        fields = ['rule_confirm', 'email', 'password1', 'password2', 'name', 'phone', 'student_no', 'college',
                  'department', 'category', 'profile_pic', 'join_year', 'join_semester']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['department'] = ''

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("해당 유저의 비밀번호를 바꾸려면 우측을 클릭하세. <a href=\'../password/\'>비밀번호 변경하기</a>"))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'phone', 'student_no', 'college', 'department',
                  'category', 'profile_pic']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
