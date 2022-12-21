from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from common.mixins import GroupRequiredMixin


class Ts(TemplateView):
    template_name = 'index.html'

class Ts1(GroupRequiredMixin, TemplateView):
    group_required = ['ts1']
    template_name = 'index.html'