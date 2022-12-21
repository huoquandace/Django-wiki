from django.shortcuts import render
from django.views.generic import TemplateView


class Ts(TemplateView):
    template_name = 'index.html'