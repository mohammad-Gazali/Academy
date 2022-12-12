from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('courses/<int:cid>', views.details, name="course_details"),
    path('personal', views.personal_courses, name="course_personal"),
    path('personal/<int:cid>', views.personal_course_display, name="course_personal_display"),
    path('personal/video/<int:lid>', views.personal_course_video, name="course_personal_video")
]
