from django.db import models
from jsonschema import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

from .fields import OrderField


class ActiveQueryset(models.QuerySet):
    """overiding the base queryset"""

    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = ActiveQueryset.as_manager()

    # django-mptt install method used to create a fk
    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey("Category", null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=False)
    objects = ActiveQueryset().as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=8)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_line")
    order = OrderField(unique_for_field="product", blank=True)
    is_active = models.BooleanField(default=False)
    objects = ActiveQueryset().as_manager()

    def clean(self):
        """this function will check to make sure that the order num is not repeated"""
        query_set = ProductLine.objects.filter(product=self.product)
        for object in query_set:
            if self.id != object.id and self.order == object.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    alt_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None)
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="productline", blank=True)

    def clean(self):
        """this function will check to make sure that the order num is not repeated"""
        query_set = ProductImage.objects.filter(productlone=self.productline)
        for object in query_set:
            if self.id != object.id and self.order == object.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
