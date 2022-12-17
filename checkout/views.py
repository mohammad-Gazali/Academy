from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext as _
from django.conf import settings
from courses.models import Cart, Course
from .models import Transaction
from .forms import UserInfoForm
import stripe
import math



def stripe_config(request: HttpRequest):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY,
        'locale': _("en")
    })


def stripe_transaction(request: HttpRequest):
    transaction = make_transaction(request)

    if not transaction:
        return JsonResponse({
            "message": _("Please Enter Valid Information")
        }, status=400)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        amount=transaction.amount * 100,
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={
            'transaction': transaction.id,
            'user_id': request.user.id
        }
    )

    return JsonResponse({
        'client_secret': intent['client_secret']
    })


def make_transaction(request: HttpRequest):
    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session_id=request.session.session_key).last()
        courses = Course.objects.filter(pk__in=cart.items)

        total = 0

        for course in courses:
            total += course.price

        if total <= 0:
            return None

        return Transaction.objects.create(
            customer=form.cleaned_data,
            session=request.session.session_key,
            amount=math.floor(total),
            items=cart.items,
        )