from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.forms import ValidationError
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views import View

from google.oauth2 import id_token
from google.auth.transport import requests

from animal_finder import forms
from animal_finder import models

# Create your views here.


def index_view(request):
    context = {'login_form': forms.LoginForm}
    return render(request, 'animal_finder/index.html', context)


class RegisterView(View):
    template_name = 'animal_finder/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


@require_POST
def login_view(request):
    form = forms.LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        print(email, password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('register')


@require_POST
def login_with_google_view(request):
    token = request.POST['idtoken']
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CREDENTIALS['web']['client_id'])

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.

        # idinfo['sub']
        email = idinfo['email']
        
        user = models.MyUser.objects.get(email=email)
        
        # User exists then log in
        login(request, user)
        return redirect('index')
        # User does not exists -> create new account
    except ValueError:
        # Invalid token
        pass
    except models.MyUser.DoesNotExist:
        user_info = {}
        user_info['email'] = idinfo['email']
        user_info['name'] = idinfo['given_name']
        user_info['surname'] = idinfo['family_name']
        return redirect('register')


