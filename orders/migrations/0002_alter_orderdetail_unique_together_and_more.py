# Generated by Django 4.0.3 on 2022-03-21 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderdetail',
            unique_together={('product', 'order')},
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='price',
        ),
    ]
