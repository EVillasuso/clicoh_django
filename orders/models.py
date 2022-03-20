from decimal import Decimal
from turtle import st
from django.db import models


class Product(models.Model):
    #id autofield is automatically created on django, can be accessed by object.id or object.pk
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Product Name',
        help_text='Enter the display name for the product'
        )
    price = models.DecimalField(
        verbose_name='Price', 
        max_digits=10, 
        decimal_places=2,
        help_text='Enter the current price for the product'
        ) # Note: DecimalField is a field prepared for money, decimal type is better than float
    stock = models.PositiveIntegerField(verbose_name='Stock')
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('name',)


class Order(models.Model):
    date_time = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Date and Time',
        help_text='Enter the date and time of the order, default is current date and time',
        )
    
    def __str__(self) -> str:
        return f'Order #{self.pk}'
    
    class Meta:
        ordering = ('-date_time',)
    
    #custom methods over here:
    def get_total(self) -> Decimal:
        total = 0
        for detail in self.details.all():
            total += detail.get_subtotal()
        return total
    
    def get_total_usd(self) -> Decimal:
        usd_value = 200 #ToDo: Use api. Issued: https://github.com/EVillasuso/clicoh_django/issues/2
        return self.get_total * usd_value
class OrderDetail(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
        )
    quantity = models.PositiveIntegerField(help_text='Enter the quantity of the product')
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='details'
        )
    price = models.DecimalField(
        verbose_name='Price', 
        max_digits=10, 
        decimal_places=2,
        help_text='The price of the selected product at the moment of the order'
        ) # Note: this field is not in the original model, but it is added because is needed to maintain the original price at the order time. A 'factura' cannot vary their own total price in time, must be maintained.
    
    def __str__(self) -> str:
        return f'{self.product.name} - {self.quantity}'
    
    class Meta:
        ordering = ('-order', '-pk')
    
    #custom methods over here:
    def get_subtotal(self) -> Decimal:
        return self.price * self.quantity
