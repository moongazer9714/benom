from django.db.models import fields
from django.db.models.expressions import F
from django.forms import widgets
from django.forms.models import _Labels
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
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('username was taken')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('email was taken')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'type')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class SellerAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Seller
        fields = ('username', 'email', 'first_name', 'phone_number',)
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        seller = super(SellerAdminCreationForm, self).save(commit=False)
        seller.set_password(self.cleaned_data['password1'])
        seller.save()
        SellerMore.objects.create(user=seller)
        return seller


class CustomerAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('username', 'email', 'first_name', 'last _name', 'phone_number',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        customer = super(CustomerAdminCreationForm, self).save(commit=False)
        customer.set_password(self.cleaned_data['password1'])
        customer.save()
        CustomMore.objects.create(user=customer)
        return customer


class ModeratorAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Moderator
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        moderator = super(ModeratorAdminCreationForm, self).save(commit=False)
        moderator.set_password(self.cleaned_data['password1'])
        moderator.is_staff=True
        moderator.save()
        ModeratorMore.objects.create(user=moderator)
        return moderator


class AdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        admin = super(AdminCreationForm, self).save(commit=False)
        admin.set_password(self.cleaned_data['password1'])
        admin.is_staff=True
        admin.is_superuser=True
        admin.save()
        AdminMore.objects.create(user=admin)
        return admin


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"
    
    def clean_password(self):
        return self.initial["password"]

    
class SellerAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Seller
        fields = "__all__"
    
    def clean_password(self):
        return self.initial['password']


class CustomerAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Customer
        fields = "__all__"

    def clean_password(self):
        return self.initial['password']


class ModeratorAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Moderator
        fields = "__all__"

    def clean_password(self):
        return self.initial['password']


class AdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Admin
        fields = "__all__"

    def clean_password(self):
        return self.initial['password']

        

