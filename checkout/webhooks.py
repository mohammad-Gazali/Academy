from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from courses.models import Course, Cart
from .models import Transaction, TransactionStatus
import stripe


@csrf_exempt
def stripe_webhook(request: HttpRequest):
    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )

    except ValueError:
        print("Invalid payload")
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        print("Invalid signature")
        return HttpResponse(status=400)


    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event.data.object
        print("payment_intent.succeeded")
        transaction_id = payment_intent.metadata.transaction
        user_id = payment_intent.metadata.user_id
        make_order(transaction_id, user_id)

        transaction = Transaction.objects.get(pk=int(transaction_id))

        session_id = transaction.session

        cart = Cart.objects.filter(session_id=session_id).last()
        cart.delete()
    else:
      print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)



def make_order(tid, uid):
    transaction = Transaction.objects.get(pk=int(tid))

    transaction.status = TransactionStatus.Completed

    transaction.save()

    courses = Course.objects.filter(pk__in=transaction.items)

    # make the course valid for the customer
    for course in courses:
        course.users = course.users | { uid: "valid" }
        course.save()
        course.transactioncourse_set.create(
            transaction_id=tid,
            course_id=course.id,
            price=course.price
        )

    return redirect('checkout_complete')