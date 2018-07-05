from django import forms
from .models import User


class AuthenticationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
