from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.db import transaction

from orders.models import Order, OrderDetail, Product

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2,)
    stock = serializers.IntegerField()
    
    class Meta:
        model = Product
        fields = '__all__'

    
class OrderDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
    class Meta:
        model = OrderDetail
        fields = ('id', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)
    date_time = serializers.DateTimeField()
    # allow to pass orderdetails
    details = OrderDetailSerializer(many=True, read_only=False)
    get_total = serializers.ReadOnlyField()
    get_total_usd = serializers.ReadOnlyField()
    
    @transaction.atomic #if an error returned (i.e. out of stock) the transaction will be rolled back
    def update(self, instance, validated_data):
        instance.date_time = validated_data.get('date_time', instance.date_time) # update time
        
        details_data = validated_data.get('details', []) # get details data
        if len(details_data)==0: # all orders must have at least one detail
            raise ValidationError('Order must have at least one detail')
        
        for detail in instance.details.all():
            product = Product.objects.get(pk=detail.product.pk)
            product.stock = product.stock + detail.quantity
            product.save()
            detail.delete()
            
        details_data = validated_data.get('details', [])
        for detail in details_data:
            if detail.quantity > 0: # controls that the quantity is at least one, if not, dont add the record. Only PossitiveIntegers is allowed.
                product = Product.objects.get(pk=detail['product'].pk)
                if product.stock >= detail['quantity']:
                    product.stock -= detail['quantity']
                    product.save()
                    OrderDetail.objects.create(**detail, order=instance)
                else:
                    raise ValidationError(f'Product {product.name} out of stock')
            
        return instance
    
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        if len(details_data)==0: # all orders must have at least one detail
            raise ValidationError('Order must have at least one detail')
        order = Order.objects.create(**validated_data)
        for detail in details_data:
            product = detail['product']
            if product.stock >= detail['quantity']:
                product.stock -= detail['quantity']
                product.save()
                OrderDetail.objects.create(**detail, order=order)
            else:
                raise ValidationError(f'Product {product.name} out of stock')
        return order

    
    class Meta:
        model = Order
        fields = '__all__'
