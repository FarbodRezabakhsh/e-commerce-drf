"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from apps.cart import views
from apps.catalog.views import ProductViewSet, CategoryViewSet
from apps.cart.views import CartDetailView, CartItemUpdateView, CartItemAddView

router = DefaultRouter()
router.register('products', ProductViewSet, basename="product")
router.register('category', CategoryViewSet, basename="category")

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path("api/cart/",views.CartDetailView.as_view(), name="cart-detail"),
    path("api/cart/items/",views.CartItemAddView.as_view(), name="cart-add-item"),
    path("api/cart/items/<uuid:item_id>/", CartItemUpdateView.as_view(), name="cart-item-update"),
]

if settings.DEBUG:                         # only in dev
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)