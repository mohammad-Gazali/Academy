from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .models import Course



def index(request: HttpRequest):
    print(request.user)
    courses = Course.objects.all()
    return render(request, 'index.html', {"courses": courses})


def details(request: HttpRequest, cid):
    course = Course.objects.get(pk=cid)
    return render(request, 'details.html', {"course": course})