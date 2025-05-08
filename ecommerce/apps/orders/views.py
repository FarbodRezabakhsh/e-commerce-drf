from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from apps.cart.models import Cart
from apps.payments.models import Payment
from apps.orders.models import Order, OrderItem
from apps.payments.zarinpal import request_payment, verify_payment
from rest_framework import status, permissions

# Create your views here.

class CheckoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if cart.items().count() == 0:
            return Response({"Detail":"Cart is empty"},status=status.HTTP_404_NOT_FOUND)
        order = Order.objects.create(user=request.user, total_price=cart.grand_total)
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                variant=item.variant,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            )
            for item in cart.items.all()
        ])

        authority, pay_url = request_payment(
            amount=order.total_price,
            description=f"Order {order.id}",
            email=request.user.email,
        )
        Payment.objects.create(order=order, authority=authority)
        cart.items.all().delete()

        return Response({"pay_url":pay_url}, status=201)


