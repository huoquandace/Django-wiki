from django.shortcuts import render
from django.views.generic import ListView


from authentication.models import User

# Create your views here.

class UserList(ListView):
    template_name = 'index1.html'
    model = User
    context_object_name = 'objects'