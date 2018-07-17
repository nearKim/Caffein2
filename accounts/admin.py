from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    ActiveUser
)

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'name', 'phone', 'student_no', 'college',
                    'department', 'category')
    list_filter = ('college', 'department', 'category')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('개인정보'), {'fields': ('name', 'phone', 'profile_pic')}),
        (_('학적정보'), {'fields': ('student_no', 'college', 'department', 'category')}),
        (_('권한'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('중요 날짜'), {'fields': ('join_year', 'join_semester', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password')}),
        (_('개인정보'), {'fields': ('name', 'phone', 'profile_pic')}),
        (_('학적정보'), {'fields': ('student_no', 'college', 'department', 'category')}),
        (_('권한'), {'fields': ('is_active', 'is_staff')}),
        (_('중요 날짜'), {'fields': ('join_year', 'join_semester')})
    )
    search_fields = ('email',)
    ordering = ('date_joined',)


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(ActiveUser)
