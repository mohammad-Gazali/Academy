from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf.global_settings import AUTH_USER_MODEL
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Article(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=255, unique=True)
    body = RichTextField()
    is_arabic = models.BooleanField(default=True, verbose_name=_('is arabic'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    author = models.ForeignKey(AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name=_('author'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('category'))


    def __str__(self):
        return f"({self.id})- {self.title}"


    def author_name(self):
        return self.author.username


    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')