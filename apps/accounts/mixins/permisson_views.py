from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from common.mixins import GroupRequiredMixin


class Ts(PermissionRequiredMixin, TemplateView):
    permission_required = ['authentication.add_profile', ]
    template_name = 'index.html'

class Ts1(GroupRequiredMixin, TemplateView):
    group_required = ['ts1']
    template_name = 'index.html'