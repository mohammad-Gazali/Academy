from django.contrib import admin
from . import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ['name', 'short_description', 'description', 'thumbnail_image', 'price']


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_at']
    list_filter = ['course']
    ordering = ['course']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'created_at']
    list_filter = ['lesson']
    ordering = ['lesson']


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    pass