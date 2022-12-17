from django.urls import path
from courses.views import checkout, checkout_complete
from . import views, webhooks


urlpatterns = [
    path('', checkout, name="checkout"),
    path('complete', checkout_complete, name="checkout_complete"),
    path('stripe', views.stripe_transaction, name="checkout_stripe"),
    path('stripe/config', views.stripe_config, name="checkout_stripe_config"),
    path('stripe/webhook', webhooks.stripe_webhook, name="checkout_stripe_webhook")
]
