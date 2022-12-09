from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Article
from .forms import ArticleForm


def list_blog(request: HttpRequest):
    articles = Article.objects.all()
    return render(request, 'main_blog.html', {"articles": articles})


@login_required
def create_blog(request: HttpRequest):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            body = form.cleaned_data['body']
            is_arabic = form.cleaned_data['is_arabic']
            Article.objects.create(
                title=title,
                category=category,
                body=body,
                is_arabic=is_arabic,
                author=request.user
            )
        return redirect('home')
    else:
        return render(request, 'create_blog.html', {"form": form})


@login_required
def list_person_articles(request: HttpRequest):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'personal_blog.html', {'articles': articles})



class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    