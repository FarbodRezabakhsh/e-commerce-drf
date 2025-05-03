from django.shortcuts import render
from rest_framework import generics, status, permissions
from .models import Cart
from uuid import UUID
from .serializers import CartItemReadSerializer, CartSerializer, CartItemWriteSerializer
from rest_framework.response import Response


# Create your views here.


def _get_or_create_cart(request):
    cart_id = request.COOKIES.get('cart_id')
    cart = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if cart_id:
            try:
                cart = Cart.objects.get(id=UUID(cart_id))
            except (Cart.DoesNotExist, ValueError):
                pass
        if cart is None:
            cart = Cart.objects.create()
    return cart

class CartDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CartSerializer

    def get_object(self):
        return _get_or_create_cart(self.request)

    def finalize_response(self, request, response, *args, **kwargs):
        cart = self.get_object()
        response = super().finalize_response(request, response, *args, **kwargs)
        if not request.user.is_authenticated:
            response.set_cookie("cart_id", cart.id, max_age=60 * 60 * 24 * 30) # set cookie for 30 days
        return response


class CartItemAddView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CartItemWriteSerializer

    def perform_create(self, serializer):
        cart = _get_or_create_cart(self.request)
        serializer.save(cart=cart)

    def finalize_response(self, request, response, *args, **kwargs):
        cart = _get_or_create_cart(self.request)
        response = super().finalize_response(request, response, *args, **kwargs)
        if not request.user.is_authenticated:
            response.set_cookie("cart_id", cart.id, max_age=60 * 60 * 24 * 30)
        return response

class CartItemUpdateView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CartItemWriteSerializer
    lookup_url_kwarg = "cart_id"

    def get_queryset(self):
        cart = _get_or_create_cart(self.request)
        return cart.items.all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return CartItemWriteSerializer
        return CartItemReadSerializer
