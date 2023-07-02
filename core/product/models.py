from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    # django-mptt install method used to create a fk
    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # links products to brand via fk
    category = TreeForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )  # links products to category
    is_active = models.BooleanField(default=False)
    # is_active allows us to filter products that are only
    # active and we can toggle this functionality

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(
        decimal_places=2, max_digits=5
    )  # 5 digit max for prices
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    # on_delete of a product curently will also delete the product line
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
