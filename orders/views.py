from rest_framework import viewsets
from django.db import transaction

from orders.models import Order, Product
from orders.serializers import OrderSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['name']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    search_fields = ['id', 'time_date']
    
    @transaction.atomic
    def destroy(self, request, pk, *args, **kwargs):
        instance = Order.objects.get(pk=pk)
        for detail in instance.details.all():
            product = Product.objects.get(pk=detail.product.pk)
            product.stock += detail.quantity
            product.save()
            detail.delete()
        return super().destroy(request, pk, *args, **kwargs)