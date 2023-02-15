import json, requests

from django.views.generic import *
from django.shortcuts import render, HttpResponse


class UserListView(View):
    def get(self, request, id=None):
        response = requests.get('http://localhost:8000/api/users/')
        data = response.json()
        return render(request, 'u-list.html', {
            "data": data
        })
    def post(self, request):
        payload = {
            'username': request.POST.get("username"),
            'password': request.POST.get("password")
        }
        response = requests.post('http://localhost:8000/api/users/', data=payload)
        if response.status_code == 201:
            return render(request, 'u-list.html' , {
                "status": "OK",
            })
        else:
            return render(request, 'u-list.html' , {
                "status": "NG",
            })