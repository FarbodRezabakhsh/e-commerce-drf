from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from .zarinpal import verify_payment
from apps.orders.models import Order
from .models import Payment
from django.utils import timezone

# Create your views here.

class VerifyPaymentView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        authority = request.GET.get('authority')
        status_flag = request.GET.get('Status')
        payment = get_object_or_404(Payment, authority=authority)
        order = payment.order

        if status_flag != "OK":
            payment.status = "nok"
            order.status = Order.FAILED
            order.save(), payment.save()
            return redirect("/payment/fail/")

        ok, ref_id = verify_payment(authority, order.total_price)
        if ok:
            payment.status, payment.ref_id, payment.paid_at = "ok", ref_id, timezone.now()
            order.status = Order.PAID
        else:
            payment.status, order.status = "nok", Order.FAILED
        order.save(), payment.save()
        return redirect("/payment/success/")


