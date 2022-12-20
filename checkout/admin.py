from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_email', 'customer_name', 'amount', 'status', 'created_at']
    list_filter = ['status']
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False