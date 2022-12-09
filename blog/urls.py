from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_blog, name='blog_list'),
    path('create', views.create_blog, name='blog_create'),
    path('personal', views.list_person_articles, name='blog_personal')
]
