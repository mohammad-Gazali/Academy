from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from courses.models import Course
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
        make_order(transaction_id, str(request.user.id))

    else:
      print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)



def make_order(tid, uid):
    transaction = Transaction.objects.get(pk=tid)

    transaction.status = TransactionStatus.Completed

    transaction.save()

    courses = Course.objects.filter(pk__in=transaction.items)

    # make the course valid for the customer
    for course in courses:
        course.users = course.user | { uid: "valid" }
        course.save()
        course.transactioncourse_set.create(
            course_id=course.id,
            price=course.price
        )

    return redirect('checkout_complete')