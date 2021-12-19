from django.db.models import fields
from rest_framework.permissions import BasePermission
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email',)