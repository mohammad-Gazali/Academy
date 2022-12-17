from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass