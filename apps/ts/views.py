from django.shortcuts import render

from ts.models import *


def index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html',{'posts':posts})