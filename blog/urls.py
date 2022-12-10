from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_blog, name='blog_list'),
    path('personal', views.list_person_articles, name='blog_personal'),
    path('detail/<int:aid>', views.article_detail, name='blog_detail'),
    path('create', views.create_blog, name='blog_create'),
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='blog_delete'),
]
