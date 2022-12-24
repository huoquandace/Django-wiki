from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    # def get(self, request, *args, **kwargs):
    #     messages.info(request, 'success')
    #     return render(request, 'index.html')