from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('<int:cid>', views.details, name="course_details"),
]
