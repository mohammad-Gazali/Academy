from django.http import HttpRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from .my_functions import get_valid_courses
from .models import Course, Lesson, Comment, Cart
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


@login_required
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
                related_comment_id = None
                related_comment = None
                if request.POST.get('comment-id') != '':
                    related_comment_id = int(request.POST.get('comment-id'))
                    related_comment = Comment.objects.get(pk=related_comment_id).content
                Comment.objects.create(
                    content=content, 
                    lesson=lesson,
                    user=user,
                    related_comment_id=related_comment_id,
                    related_comment=related_comment,
                )
                return redirect(f'/personal/video/{lesson.id}')
        else:
            form = CommentCreateForm()
            return render(request, 'courses_video.html', {'lesson': lesson, 'form': form})
    else:
        return HttpResponseForbidden("<h1>403</h1><h1>Forbidden</h1>")


@login_required
def delete_comment(request: HttpRequest, cid):
    valid_courses = get_valid_courses(request.user)
    comment = Comment.objects.get(pk=cid)
    course = comment.lesson.course
    if course in valid_courses:
        if request.method == "POST":
            comment.delete()
            return redirect(f'/personal/video/{comment.lesson.id}')
        else:
            return HttpResponseNotAllowed("<h1>405</h1><h1>Not Allowed Method</h1>")
    else:
        return HttpResponseForbidden("<h1>403</h1><h1>Forbidden</h1>")



def cart_update(request: HttpRequest, cid):
    if request.method == "GET":
        if request.user.is_authenticated:
            if not request.session.session_key:
                request.session.create()
            session_id = request.session.session_key

            cart_model = Cart.objects.filter(session_id=session_id).last()

            course = Course.objects.get(pk=cid)

            if str(request.user.id) in course.users:
                if cart_model is None:
                    return JsonResponse({
                    "title": _("Course Has Repeated"),
                    "message": _("You Have This Course, Check Your Personal Courses"),
                    "button": _("Continue"),
                    "items_count": 0,
                    "icon": "info"
                    })
                else:
                    return JsonResponse({
                    "title": _("Course Has Repeated"),
                    "message": _("You Have This Course, Check Your Personal Courses"),
                    "items_count": len(cart_model.items),
                    "button": _("Continue"),
                    "icon": "info"
            })

        else:
            return JsonResponse({
                "title": _("Login Is Required"),
                "message": _("You Should Either Login or Create a New Account"),
                "items_count": 0,
                "button": _("Continue"),
                "icon": "info"
            })


        if cart_model is None:
            cart_model = Cart.objects.create(
                session_id=session_id,
                items=[cid]
            )
        elif cid not in cart_model.items:
            cart_model.items.append(cid)
            cart_model.save()


        return JsonResponse({
            "title": _("Success"),
            "message": _("The Course Has Been Added Successfully to the Cart"),
            "items_count": len(cart_model.items),
            "button": _("Continue")
        })
    else:
        return HttpResponseNotAllowed("<h1>405</h1><h1>Not Allowed Method</h1>")


@login_required
def delete_from_cart(request: HttpRequest, cid):
    if request.method == "GET":
        session_id = request.session.session_key
        if not session_id:
            return JsonResponse({})
        cart = Cart.objects.filter(session_id=session_id).last()

        if cid in cart.items:
            cart.items.remove(cid)
            cart.save()
        
        return JsonResponse({})
    else:
        return HttpResponseNotAllowed("<h1>405</h1><h1>Not Allowed Method</h1>")


@login_required
def reset_cart(request: HttpRequest):
    if request.method == "GET":
        session_id = request.session.session_key
        if not session_id:
            return JsonResponse({})
        cart = Cart.objects.filter(session_id=session_id).last()
        cart.delete()
        return JsonResponse({})
    else:
        return HttpResponseNotAllowed("<h1>405</h1><h1>Not Allowed Method</h1>")


@login_required
def cart(request: HttpRequest):
    return render(request, "cart.html")


@login_required
def checkout(request: HttpRequest):
    return render(request, "checkout/checkout.html")


@login_required
def checkout_complete(request: HttpRequest):
    return render(request, "checkout/checkout_complete.html")