from rest_framework import serializers
from .models import Cart, CartItem
from apps.catalog.serializers import ProductVariantSerializer

class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'variant', 'quantity')


class CartItemReadSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    unit_price = serializers.IntegerField(read_only=True)
    total_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'variant', 'quantity', 'unit_price', 'total_price')

class CartItem(serializers.ModelSerializer):
    items = CartItemReadSerializer(many=True, read_only=True)
    subtotal = serializers.IntegerField(read_only=True)
    shipping_fee = serializers.IntegerField(read_only=True)
    grand_total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'subtotal', 'shipping_fee', 'grand_total')

