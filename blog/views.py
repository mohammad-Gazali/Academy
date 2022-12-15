from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest
from .models import Article
from .forms import ArticleForm


def list_blog(request: HttpRequest):
    articles = Article.objects.all().order_by("-created_at")
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


@login_required
def article_detail(request: HttpRequest, aid):
    article = Article.objects.get(pk=aid)
    return render(request, 'detail_blog.html', {'article': article})


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = "update_blog.html"
    form_class = ArticleForm

    def test_func(self):
        return self.request.user == self.get_object().author
    
    def get_success_url(self):
        return reverse('blog_update', args=[self.object.id])


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'delete_blog.html'
    success_url = reverse_lazy('blog_personal')

    def test_func(self):
        return self.request.user == self.get_object().author