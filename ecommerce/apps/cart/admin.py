from django.contrib import admin
from .models import CartItem, Cart


# Register your models here.

class CartItemInLine(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['unit_price', 'total_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subtotal', 'grand_total','created_at']
    inlines = (CartItemInLine,)
    readonly_fields = ['subtotal', 'shipping_fee', 'grand_total']