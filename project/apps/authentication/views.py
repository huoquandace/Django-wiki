from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView


class Login(LoginView):
    template_name = 'login.html'

class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'