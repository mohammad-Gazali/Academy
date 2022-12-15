from .models import Course, Cart

def academy_website(request):
    cart = Cart.objects.filter(session=request.session.session_key).last() or None

    cart_total = 0
    cart_courses = []

    if cart is not None:
        cart_courses = Course.objects.filter(pk__in=cart.items)
        for course in cart_courses:
            cart_total += course.price

    return {
        "cart_courses": cart_courses,
        "cart_total": cart_total
    }