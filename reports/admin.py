from django.utils.translation import gettext as _
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek
from django.template.response import TemplateResponse
from django.db.models import Sum
from django.contrib import admin
from django.http import HttpRequest
from .models import OrderReport
from checkout.models import Transaction
import json


@admin.register(OrderReport)
class OrderReportAdmin(admin.ModelAdmin):
    
    change_list_template = 'admin/reports/orders.html'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request: HttpRequest, extra_context=None):
        
        yearly_stats = (
            Transaction.objects
            .annotate(year=ExtractYear("created_at"))
            .values("year")  
            .annotate(sum=Sum("amount"))
        )

        monthly_stats = (
            Transaction.objects.select_related("transaction")
            .annotate(year=ExtractYear("created_at"))
            .annotate(month=ExtractMonth("created_at"))
            .values("year", "month")  
            .annotate(sum=Sum("amount"))[:30]  
        )

        weekly_stats = (
            Transaction.objects.select_related("transaction")
            .annotate(year=ExtractYear("created_at"))
            .annotate(week=ExtractWeek("created_at"))
            .values("year", "week")
            .annotate(sum=Sum("amount"))[:30]
        )


        context = {
            **self.admin_site.each_context(request),
            "title": _("Orders Report"),
            "yearly_stats": json.dumps(list(yearly_stats)),
            "monthly_stats": json.dumps(list(monthly_stats)),
            "weekly_stats": json.dumps(list(weekly_stats))
        }


        return TemplateResponse(
            request, 
            self.change_list_template,
            context
        )


