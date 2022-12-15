from django.db import models
from django.contrib.sessions.models import Session
from django.conf.global_settings import AUTH_USER_MODEL
from django.utils.translation import gettext as _
from main import settings


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    short_description = models.CharField(max_length=255, verbose_name=_('short description'))
    description = models.TextField(verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    thumbnail_image = models.ImageField(verbose_name=_('thumbnail image'))
    price = models.FloatField(verbose_name=_('price'))
    users = models.JSONField(default=dict)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    video = models.FileField(verbose_name=_('video'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('course'))


    @property
    def video_url(self):
        return settings.SITE_URL + self.video.url

    def __str__(self):
        return self.title


    class META:
        verbose_name = _('lesson')
        verbose_name_plural = _('lessons')


class Comment(models.Model):
    content = models.TextField(verbose_name=_('content'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=_('lesson'))
    related_comment_id = models.IntegerField(verbose_name=_('related comment id'), null=True, blank=True)
    related_comment = models.TextField(verbose_name=_('related comment'), null=True, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'), null=True, blank=True)


    def __str__(self):
        return f"Comment ({self.id})" 

    class META:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Cart(models.Model):
    items = models.JSONField(default=list)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name=_("session"))

    class META:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


