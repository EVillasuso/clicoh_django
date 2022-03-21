from decimal import Decimal
from django.db import models

from django.conf import settings


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
        """
        Returns the total price of the order
        """
        total = 0
        for detail in self.details.all():
            total += detail.get_subtotal()
        return total
    
    def get_total_usd(self) -> Decimal:
        """
        Returns the total price of the order in USD.
        Takes the current price in ARS from get_total() and converts it to USD
        Uses utils.USD_FETCHER to fetch the current 'Dolar Blue' price
        """
        usd_value = settings.USD_FETCHER.get_dolar_blue()
        return self.get_total() / usd_value
    
    
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
    
    def __str__(self) -> str:
        return f'{self.product.name} - {self.quantity}'
    
    class Meta:
        ordering = ('-order', '-pk')
        unique_together = ('product', 'order') # grants that the same order cant contains 2 details for the same product
    
    #custom methods over here:
    def get_subtotal(self) -> Decimal:
        """
        Returns the subtotal of the order detail (order line) in Decimal.
        """
        return self.product.price * self.quantity
