from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .my_functions import get_valid_courses
from .models import Course, Lesson, Comment
from .forms import CommentCreateForm


def index(request: HttpRequest):
    courses = Course.objects.all()
    return render(request, 'index.html', {"courses": courses})


def details(request: HttpRequest, cid):
    course = Course.objects.get(pk=cid)
    return render(request, 'courses_details.html', {"course": course})


@login_required
def personal_courses(request: HttpRequest):
    courses = get_valid_courses(request.user)
    return render(request, 'courses_personal.html', {"courses": courses})


@login_required
def personal_course_display(request: HttpRequest, cid):
    valid_courses = get_valid_courses(request.user)
    course = Course.objects.get(pk=cid)
    if course in valid_courses:
        return render(request, 'courses_personal_display.html', {'course': course})
    else:
        return HttpResponseForbidden("<h1>403</h1><h1>Forbidden</h1>")


def personal_course_video(request: HttpRequest, lid):
    valid_courses = get_valid_courses(request.user)
    lesson = Lesson.objects.get(pk=lid)
    course = Course.objects.get(pk=lesson.course_id)
    if course in valid_courses:
        if request.method == "POST":
            form = CommentCreateForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data["content"]
                user = request.user
                print(content)
                Comment.objects.create(
                    content=content, 
                    lesson=lesson,
                    user=user
                )
                return redirect(f'/personal/video/{lesson.id}')
        else:
            form = CommentCreateForm()
            return render(request, 'courses_video.html', {'lesson': lesson, 'form': form})
    else:
        return HttpResponseForbidden("<h1>403</h1><h1>Forbidden</h1>")


