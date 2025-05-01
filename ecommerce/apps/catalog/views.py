from rest_framework import viewsets, permissions
from .models import Category, ProductVariant, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer


# Create your views here.

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('children').all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('variants','images')
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

    
