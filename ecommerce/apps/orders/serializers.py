from rest_framework import serializers
from .models import Order, OrderItem
from apps.payments.serializers import PaymentSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("variant", "quantity", "unit_price", "total_price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "total_price", "status", "created_at", "items", "payment")