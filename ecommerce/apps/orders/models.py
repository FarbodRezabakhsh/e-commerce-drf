from django.db import models
from django.conf import settings
from apps.catalog.models import ProductVariant

# Create your models here.

class Order(models.Model):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
        (FAILED, "Failed"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    total_price = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self):
        return f"{self.variant.sku} × {self.quantity}"
