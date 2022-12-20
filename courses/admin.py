from django.contrib import admin
from . import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ['name', 'short_description', 'description', 'name_arabic', 'short_description_arabic', 'description_arabic', 'thumbnail_image', 'price']
    list_display = ['name', 'name_arabic', 'created_at', 'updated_at', 'price']


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_at']
    list_filter = ['course']
    ordering = ['course']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'created_at']
    list_filter = ['lesson']
    search_fields = ['user']
    ordering = ['lesson']
