from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import ValidationError
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
    register_form = forms.RegisterForm

    def get(self, request):
        form = self.register_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.register_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})


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
        return HttpResponse(status=200)
    except ValueError:
        # Invalid token
        pass
    # User does not exists -> create new account
    except models.MyUser.DoesNotExist:
        response = {}
        response['email'] = idinfo['email']
        response['name'] = idinfo['given_name']
        response['surname'] = idinfo['family_name']
        response['redirect_url'] = reverse('register')
        return HttpResponse(user_info, status=302)


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    context = {}
    user = request.user
    animals = models.Animal.objects.filter(owner=user)
    context['animals'] = animals
    return render(request, 'animal_finder/profile.html', context)


class AddAnimalView(LoginRequiredMixin,View):
    add_animal_form = forms.AddAnimalForm
    template_name = 'animal_finder/add_animal.html'

    def get(self,request):
        context = {}
        context['form'] = self.add_animal_form()
        return render(request, self.template_name, context)
    
    def post(self, request,*args, **kwargs):
        print(request, args, kwargs)
        print(request.POST)
        form = self.add_animal_form(request.POST)
        print("here22")
        if form.is_valid():
            print("HERE valid")
            animal = form.save(commit=False)
            animal.owner = request.user
            animal.save()
            return redirect('profile')
        else:
            print("HERE notvalid")
            return render(request, self.template_name, {'form':form})