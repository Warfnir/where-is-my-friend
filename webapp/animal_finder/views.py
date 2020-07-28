from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login

from animal_finder import forms
from animal_finder import models

# Create your views here.
def index_view(request):
    context = {'login_form': forms.LoginForm}
    return render(request, 'animal_finder/index.html', context)


@require_POST
def login_view(request):
    form = forms.LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        print(email, password)
        # login user and return
