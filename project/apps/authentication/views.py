from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView

from authentication.forms import *


class Login(LoginView):
    template_name = 'login.html'

class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        data = form.cleaned_data
        from pprint import pprint
        pprint(data)
        pass

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'