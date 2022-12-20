from django import template
from checkout.models import Transaction

register = template.Library()

def currency(amount):
    return "{:.2f}".format(amount) + ' $'

def course_title(title):
    return title[4:]

def get_items(transaction_id):
    transaction = Transaction.objects.get(pk=int(transaction_id))
    transaction_course_items = transaction.transactioncourse_set.all()
    return transaction_course_items

register.filter('currency', currency)
register.filter('course_title', course_title)
register.filter('get_items', get_items)