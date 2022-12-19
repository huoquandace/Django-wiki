from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class Login(LoginView):
    template_name = 'login.html'

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'