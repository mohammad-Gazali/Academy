from django.db import models
from django.utils.translation import gettext_lazy as _


class TransactionStatus(models.IntegerChoices):
    Pending = 0, _("Pending")
    Completed = 1, _("Completed")


class Transaction(models.Model):
    session = models.CharField(max_length=255)
    amount = models.FloatField(verbose_name=_("amount"))
    items = models.JSONField(default=list, verbose_name=_("items"))
    customer = models.JSONField(default=dict, verbose_name=_("customer"))
    status = models.IntegerField(choices=TransactionStatus.choices, default=TransactionStatus.Pending, verbose_name=_("status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))   
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    @property
    def customer_name(self):
        return self.customer['first_name'] + ' ' + self.customer['last_name']
    customer_name.fget.short_description = _('customer name')


    @property
    def customer_email(self):
        return self.customer['email']
    customer_email.fget.short_description = _('customer email')

    def __str__(self):
        return _("Transaction") + f" {self.id}"


    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")