from django.db import models
from django.conf import settings
import uuid
from apps.catalog.models import ProductVariant

# Create your models here.
SHIPPING_FEE = 80000

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def shipping_fee(self):
        return SHIPPING_FEE

    @property
    def grand_total(self):
        return self.subtotal + self.shipping_fee

    def __str__(self):
        return f"Cart: {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('cart', 'variant'),)

    @property
    def unit_price(self):
        return self.variant.price

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f'{self.variant.sku} x {self.quantity}'