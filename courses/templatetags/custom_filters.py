from django import template

register = template.Library()

def currency(amount):
    return "{:.2f}".format(amount) + ' $'

def course_title(title):
    return title[4:]

register.filter('currency', currency)
register.filter('course_title', course_title)