from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('courses/<int:cid>', views.details, name="course_details"),
]
