from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment')
    authority = models.CharField(max_length=64, unique=True)
    ref_id = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=12, default='init')
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.authority} ({self.status})"