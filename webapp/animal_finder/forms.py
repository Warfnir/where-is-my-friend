from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30, required=True,label="", widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':'Password'}))