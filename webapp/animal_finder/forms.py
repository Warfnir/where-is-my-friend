from django import forms
from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password

from animal_finder.models import MyUser


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30, required=True, label="",
                             widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'surname')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get("email")
    #     user = MyUser.objects.filter(email=email)
    #     print(cleaned_data, email, user)
    #     if user.exists():
    #         print("exists")
    #         raise forms.ValidationError("Email already taken.")
    #     print("went good")
    #     return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already taken.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        validate_password(password1)
        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('__all__')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'name', 'surname', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
